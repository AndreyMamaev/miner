from fastapi import HTTPException
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
import uuid

class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = 'game'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(default=False)
    mines_count: Mapped[int] = mapped_column(Integer)
    count_of_open_cells: Mapped[int] = mapped_column(Integer, default=0)

    field: Mapped[list['Cell']] = relationship(
        back_populates='game', uselist=True,
        cascade='all, delete', lazy="selectin"
    )

    @validates("width")
    def validate_width(self, key, width):
        if width < 2 or width > 30:
            raise HTTPException(
                status_code=400,
                detail="Ширина поля должан быть не менее 2 и не более 30",
            )
        return width
    
    @validates("height")
    def validate_height(self, key, height):
        if height < 2 or height > 30:
            raise HTTPException(
                status_code=400,
                detail="Высота поля должан быть не менее 2 и не более 30",
            )
        return height
    

class Cell(Base):
    __tablename__ = 'cell'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('game.id'))
    row: Mapped[int] = mapped_column(Integer)
    column: Mapped[int] = mapped_column(Integer)
    is_open: Mapped[bool] = mapped_column(default=False)
    is_bomb: Mapped[bool] = mapped_column(default=False)
    value: Mapped[str] = mapped_column(String(1))

    game: Mapped['Game'] = relationship(
        back_populates='field', uselist=False
    )