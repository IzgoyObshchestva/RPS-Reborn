from ..services.auth import verify_bot_secret

from typing import Annotated
from fastapi import Query, Depends
from ..db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud.user import UserRepository

async def get_user_id_in_db(
    user_telegtam_id: Annotated[str, Query()],
    db: AsyncSession = Depends(get_db)
):
    '''
    Получение id пользователя из БД по его telegram id
    '''
    repo = UserRepository(db)
    your_id = await repo.get_user_by_tg_id(user_telegtam_id)
    return your_id.id