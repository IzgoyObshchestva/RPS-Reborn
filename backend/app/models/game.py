from ..db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Boolean, Enum

class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)

    id_user_1: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    id_user_2: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    last_figure_1: Mapped[str] = mapped_column(Enum('Rock', 'Paper', 'Scissors', name='figure_user_1'), nullable=True)
    last_figure_2: Mapped[str] = mapped_column(Enum('Rock', 'Paper', 'Scissors', name='figure_user_2'), nullable=True)
    win_user_1: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    win_user_2: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    invitation_code: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    game_is_on: Mapped[bool] = mapped_column(Boolean, default=False)