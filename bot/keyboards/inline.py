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


next_game_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Выйти', callback_data=f'cancel_game'),
                InlineKeyboardButton(text=f'Играль дальше', callback_data=f'next_game'),
            ],
        ]
    )


join_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Выйти', callback_data=f'cancel_game'),
                InlineKeyboardButton(text=f'Играль дальше', callback_data=f'continue_game'),
            ],
        ]
    )


cancel_game_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Выйти', callback_data=f'cancel_game'),
            ],
        ]
    )