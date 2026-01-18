from fastapi import APIRouter, Depends, HTTPException, status


from ...schemas.user import CreateUser, UserResponse, UpdateUser
from ...crud.user import UserRepository

from ...db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import verify_bot_secret


router = APIRouter(dependencies=[Depends(verify_bot_secret)])

@router.post('/users/create', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUser, 
    db: AsyncSession = Depends(get_db),
):
    '''
    Создание пользователя
    
    Parameters:
        :param user_data: Данные для создание пользователя
        :type user_data: CreateUser(Request body)
            "role_name": str
            "telegram_id": int
    '''
    repo = UserRepository(db)
    existing_user = await repo.get_user_by_tg_id(user_data.telegram_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    
    new_user = await repo.create_user(user_data)
    return {
        'telegram_id': new_user.telegram_id,
        'win': new_user.win,
        'loss': new_user.loss,
        }


@router.get('/users/by_tg_id/{user_id}')
async def get_user_by_tg_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    '''
    Возвращает пользователя по telegram id
    '''
    repo = UserRepository(db)

    user_db = await repo.get_user_by_tg_id(user_id)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    return {
        'id': user_db.id,
        'telegram_id': user_db.telegram_id,
        'win': user_db.win,
        'loss': user_db.loss,
        }


@router.get('/users/by_id/{user_id}')
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    '''
    Возвращает пользователя по id из БД
    '''
    repo = UserRepository(db)

    user_db = await repo.get_user_by_id(user_id)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    return {
        'id': user_db.id,
        'telegram_id': user_db.telegram_id,
        'win': user_db.win,
        'loss': user_db.loss,
        }