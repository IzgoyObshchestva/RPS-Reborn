from pydantic import BaseModel

class GameBase(BaseModel):
    id_user_1: int
    invitation_code: str


class CreateGame(GameBase):
    pass


class GameResponse(GameBase):
    id_user_2: int
    last_figure_1: str
    last_figure_2: str
    win_user_1: int
    win_user_2: int
    game_is_on: bool

    class Config:
        from_attributes = True


class UpdateGame(BaseModel):
    id_user_1: int | None = None
    id_user_2: int | None = None
    last_figure_1: str | None = None
    last_figure_2: str | None = None
    win_user_1: int | None = None
    win_user_2: int | None = None
    invitation_code: str | None = None
    game_is_on: bool | None = None