from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from ..core.requests_to_api import get_api, post_api

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    '''
    Обработчик команды start
    '''
    json_data={
        "telegram_id": message.from_user.id,
    }
    result = await post_api(f'/users/create', json_data=json_data)

    await message.answer(
        f'Добро пожаловать в мою игру'
    )


@router.message(Command('statistics'))
async def cmd_statistics(message: Message):
    '''
    Вывод статистики
    '''
    user_tg_id = message.from_user.id

    user_db = await get_api(f'/users/by_tg_id/{user_tg_id}')

    if user_db.status_code == 200:
        await message.answer(
            'Ваша статистика:\n'
            f'🏆 Победы: {user_db.win}\n'
            f'💩 Поражения: {user_db.loss}\n'
        )
    if user_db.status_code == 404:
        await message.answer(
            f'⚠️ {user_db.detail}'
        )