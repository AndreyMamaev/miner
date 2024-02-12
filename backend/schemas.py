from pydantic import BaseModel
import uuid

class NewGameRequest(BaseModel):
    width: int
    height: int
    mines_count:int


class GameTurnRequest(BaseModel):
    game_id: uuid.UUID
    col: int
    row: int


class GameInfoResponse(BaseModel):
    game_id: uuid.UUID
    width: int
    height: int
    mines_count: int
    completed: bool
    field: list[list]