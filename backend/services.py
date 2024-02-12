from functools import lru_cache
import uuid
import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import random
import itertools

from db import get_async_session
from schemas import NewGameRequest, GameTurnRequest, GameInfoResponse
from models import Game, Cell
from utils import get_cells_around


class GameService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, game_data: NewGameRequest):
        if game_data.mines_count >= game_data.width * game_data.height - 1:
            raise HTTPException(
                status_code=400,
                detail=f'Количество мин должно быть не более {game_data.width * game_data.height - 1}.'
            )
        new_game = Game(
            width=game_data.width,
            height=game_data.height,
            mines_count=game_data.mines_count,
        )
        self.session.add(new_game)
        await self.session.flush()
        game_id = new_game.id
        cells = []
        bombs = random.sample(
            list(itertools.product(
                range(game_data.width),
                range(game_data.height)
            )),
            game_data.mines_count
        )
        for row in range(game_data.width):
            for column in range(game_data.height):
                cells.append(
                    Cell(
                        row=row,
                        column=column,
                        game_id=new_game.id,
                        is_bomb=((row, column) in bombs),
                        value=(
                            'X' if ((row, column) in bombs)
                            else str(len(set(get_cells_around(row, column)) & set(bombs)))
                        )
                    )
                )
        self.session.add_all(cells)
        return game_id
        
    async def get_game_field_by_id(self, game_id: uuid.UUID, game_over: bool=False):
        game = await self.session.get(Game, game_id, options=(
            selectinload(Game.field),
        ))
        field = [[' '] * game.width for _ in range(game.height)]
        for cell in game.field:
            if cell.is_open or game.completed:
                field[cell.row][cell.column] = cell.value
            if cell.is_bomb:
                if not game_over and game.completed:
                    field[cell.row][cell.column] = 'M'
        return GameInfoResponse(
            game_id=game.id,
            width=game.width,
            height=game.height,
            mines_count=game.mines_count,
            completed=game.completed,
            field=field
        )
    
    async def game_turn(self, turn_data: GameTurnRequest):
        game = await self.session.get(Game, turn_data.game_id, options=(
            selectinload(Game.field),
        ))
        if game.completed:
            raise HTTPException(
                status_code=400,
                detail='Игра закончена'
            )
        cell = (await self.session.execute(
            select(Cell).where(
                (Cell.game_id == turn_data.game_id) &
                (Cell.row == turn_data.row) &
                (Cell.column == turn_data.col)
            )
        )).scalar_one_or_none()
        if cell.is_open:
            raise HTTPException(
                status_code=400,
                detail='Ячейка уже открыта.'
            )
        game_over = False
        field_list = [[' '] * game.width for _ in range(game.height)]
        for cell in game.field:
            field_list[cell.row][cell.column] = cell.value
        opened_cells = (
            await self.open_cell(
                coord=(turn_data.row, turn_data.col),
                field_list=field_list,
                coord_list=[]
            )
        )
        logging.error(f'{opened_cells=}')
        for coord in set(opened_cells):
            cell = (await self.session.execute(
                select(Cell).where(
                    (Cell.game_id == turn_data.game_id) &
                    (Cell.row == coord[0]) &
                    (Cell.column == coord[1])
                )
            )).scalar_one_or_none()
            if cell:
                if cell.is_bomb:
                    game_over = True
                    break
                cell.is_open = True
                game.count_of_open_cells += 1
        if (
            game.count_of_open_cells + game.mines_count == game.width * game.height
            or game_over
        ):
            game.completed = True
        return (await self.get_game_field_by_id(game_id=turn_data.game_id, game_over=game_over))


    async def open_cell(self, coord: tuple, field_list: list[list], coord_list=[]):
        if field_list[coord[0]][coord[1]] != '0':
            coord_list += [coord]
        else:
            cells_around = get_cells_around(coord[0], coord[1])
            coord_list += [coord]
            for c in cells_around:
                if (
                    c[0] >= 0 and
                    c[0] < len(field_list) and
                    c[1] >= 0 and
                    c[1] < len(field_list[0]) and
                    c not in coord_list
                ):
                    coord_list = (await self.open_cell(
                        coord=c,
                        field_list=field_list,
                        coord_list=coord_list
                    ))
        return coord_list


@lru_cache()
def get_game_service(
    session: AsyncSession = Depends(get_async_session),
) -> GameService:
    return GameService(session)