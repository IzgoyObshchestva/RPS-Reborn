from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


game_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'🪨', callback_data=f'figure__Rock'),
                InlineKeyboardButton(text=f'✂️', callback_data=f'figure__Scissors'),
                InlineKeyboardButton(text=f'🧻', callback_data=f'figure__Paper')
            ],
            [
                InlineKeyboardButton(text=f'❌ Отменить', callback_data=f'cancel_game')
            ]
        ]
    )