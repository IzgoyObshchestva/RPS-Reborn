from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_id: int


class CreateUser(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    win: int
    loss: int

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    telegram_id: int | None = None
    win: int | None = None
    loss: int | None = None