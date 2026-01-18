from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from .requests_to_api import get_api

async def send_to_user(
    bot: Bot,
    user_telegram_id: int,
    id_user_1: int,
    id_user_2: int,
    text: str,
    kb: str = None,
    disable_notification: bool = True,
    parse_mode: str | None = "HTML"
) -> bool:
    '''
    Функция для отправки сообщения пользователю по telegram ID
    
    :param bot: бота (присто пиши message.bot)
    :type bot: Bot

    :param user_telegram_id: telegram id которму ответили на callback
    :type user_telegram_id: int

    :param id_user_1: id пользователя из БД
    :type id_user_1: int

    :param id_user_2: id пользователя из БД
    :type id_user_2: int

    :param text: текст сообщения
    :type text: str

    :param kb: клавиатура которая будет у сообщения
    :type kb: InlineKeyboardMarkup = None

    :param disable_notification: ---
    :type disable_notification: bool = True

    :param parse_mode: ---
    :type parse_mode: str | None = "HTML"
    
    :return: True - если отправилось и False - если не отправилось
    :rtype: bool
    '''
    try:
        user_db = await get_api(f'/users/by_tg_id/{user_telegram_id}')

        if user_db.id == id_user_1:
            send_user_message = id_user_2
        else:
            send_user_message = id_user_1

        user_db = await get_api(f'/users/by_id/{send_user_message}')
        await bot.send_message(
            chat_id=user_db.telegram_id,
            text=text,
            disable_notification=disable_notification,
            parse_mode=parse_mode,
            reply_markup=kb
        )
        return True
    except TelegramForbiddenError:
        print(f"Пользователь {send_user_message} заблокировал бота")
    except TelegramAPIError as e:
        print(f"Ошибка Telegram API для {send_user_message}: {e}")
    except Exception as e:
        print(f"Не удалось отправить сообщение {send_user_message}: {e}")
    return False


async def send_photo_to_user(
    bot: Bot,
    user_telegram_id: int,
    id_user_1: int,
    id_user_2: int,
    photo_path: str,
    kb: str,
    caption: str = "",
    disable_notification: bool = True,
    parse_mode: str | None = "HTML"
) -> bool:
    '''
    Функция для отправки сообщения с картинкой пользователю по telegram ID
    
    :param bot: бота (присто пиши message.bot)
    :type bot: Bot

    :param user_telegram_id: telegram id которму ответили на callback
    :type user_telegram_id: int

    :param photo_path: название изображения
    :type photo_path: str

    :param id_user_1: id пользователя из БД
    :type id_user_1: int

    :param id_user_2: id пользователя из БД
    :type id_user_2: int

    :param caption: текст сообщения
    :type caption: str

    :param kb: клавиатура которая будет у сообщения
    :type kb: InlineKeyboardMarkup = None

    :param disable_notification: ---
    :type disable_notification: bool = True

    :param parse_mode: ---
    :type parse_mode: str | None = "HTML"
    
    :return: True - если отправилось и False - если не отправилось
    :rtype: bool
    '''
    try:
        full_path = f'temp/{photo_path}'
        user_db = await get_api(f'/users/by_tg_id/{user_telegram_id}')

        if user_db.id == id_user_1:
            send_user_message = id_user_2
        else:
            send_user_message = id_user_1

        user_db = await get_api(f'/users/by_id/{send_user_message}')
        await bot.send_photo(
            chat_id=user_db.telegram_id,
            photo=FSInputFile(full_path),
            caption=caption,
            disable_notification=disable_notification,
            reply_markup=kb,
            parse_mode="HTML" if caption else None
        )
        return True
    except TelegramForbiddenError:
        print(f"Пользователь {send_user_message} заблокировал бота")
    except TelegramAPIError as e:
        print(f"Ошибка Telegram API для {send_user_message}: {e}")
    except Exception as e:
        print(f"Не удалось отправить сообщение {send_user_message}: {e}")
    return False