from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from ..core.requests_to_api import get_api, post_api, patch_api, delete_api
from ..core.func import send_to_user, send_photo_to_user
from ..keyboards.inline import game_kb, next_game_kb, join_kb, cancel_game_kb

router = Router()

@router.message(Command('game'))
async def cmd_start_game(message: Message):
    user_tg_id = message.from_user.id

    user_db = await get_api(f'/users/by_tg_id/{user_tg_id}')

    params={
        "user_id": user_db.id,
    }

    game_db = await post_api(f'/game/create', params=params)

    if game_db.status_code == 201:
        await message.answer(
            'Вы создали игру\n'
            f'Ваш код: {game_db.invitation_code}'
        )
    elif game_db.status_code == 400:
        await message.answer(
            f'⚠️ {game_db.detail}',
            reply_markup=join_kb
        )


@router.message(Command('join'))
async def cmd_join_game(message: Message):
    user_tg_id = message.from_user.id

    user_db = await get_api(f'/users/by_tg_id/{user_tg_id}')

    args = message.text.split(' ', maxsplit=1)

    if not len(args) == 2:
        await message.reply(
            f'Для того, чтобы присоедениться к игре нужна запись:\n'
            '/join <invitation_code>'
            )
        return

    game_db = await get_api(f'/game/invitation/{args[1]}')

    if game_db.status_code == 404:
        await message.answer(
            f'⚠️ {game_db.detail}'
        )
        return
    elif game_db.status_code == 403:
        await message.answer(
            f'⚠️ {game_db.detail}'
        )
        return

    json_data={
        'id_user_2': user_db.id,
    }

    game_data = await patch_api(f'/game/join/{game_db.id}', json_data=json_data)

    if game_data.status_code == 200:
        await message.answer(
            'Вы успешно присоеденились к игре\n'
            'Теперь выберети фигуру:',
            reply_markup=game_kb
        )
        success = await send_to_user(
            bot=message.bot,          # ← вот он, берётся из message
            user_telegram_id=user_tg_id,
            id_user_1=game_data.id_user_1,
            id_user_2=game_data.id_user_2,
            text="Игра началась! 🎮\nВыберите фигуру:",
            kb=game_kb
        )
        if not success:
            await message.answer("Не смог отправить уведомление 😔")
    elif game_data.status_code == 400:
        await message.answer(
            f'⚠️ {game_data.detail}',
            reply_markup=join_kb
        )


@router.callback_query(F.data.startswith("figure__"))
async def res_update_role(callback: CallbackQuery):
    '''
    
    '''
    await callback.answer("")
    user_telegram_id = callback.from_user.id
    figure = callback.data.split('__')[1]

    params = {
        'user_tg_id': user_telegram_id,
        "figure": figure
    }

    game_data = await patch_api(f'/game/figure/', params=params)

    if game_data.last_figure_1 and game_data.last_figure_2:
        params={
            "user_telegtam_id": user_telegram_id
        }
        game_res = await post_api(f'/game/result_game/{game_data.id}', params=params)

        image_file = FSInputFile(f"temp/{game_res.img}")

        if game_res.win_id_user == None:
            res_win = None
        else:
            res_win = True if game_res.your_id == game_res.win_id_user else False

        if game_res.your_id == game_res.id_user_1:
            user_1_namber_game = '1'
            user_2_namber_game = '2'
        else:
            user_1_namber_game = '2'
            user_2_namber_game = '1'

        message_user_1 = f'Вы игрок {user_1_namber_game} - {"Ничья" if res_win == None else ('победа' if res_win else 'поражение')}\nСчёт {game_res.win_user_1}:{game_res.win_user_2}'
        message_user_2 = f'Вы игрок {user_2_namber_game} - {"Ничья" if res_win == None else ('поражение' if res_win else 'победа')}\nСчёт {game_res.win_user_1}:{game_res.win_user_2}'

        await callback.message.answer_photo(
            photo=image_file, 
            caption=f'{message_user_1}',
            reply_markup=next_game_kb
        )

        success = await send_photo_to_user(
            bot=callback.bot,          # ← вот он, берётся из message
            user_telegram_id=user_telegram_id,
            id_user_1=game_res.id_user_1,
            id_user_2=game_res.id_user_2,
            photo_path=game_res.img, 
            caption=message_user_2,
            kb=next_game_kb
        )
        if not success:
            await callback.message.answer("Не смог отправить уведомление 😔")
    else:
        await callback.message.answer(
            'Ожидаем выбор второго играка...',
            reply_markup=cancel_game_kb
        )


@router.callback_query(F.data == 'cancel_game')
async def res_update_role(callback: CallbackQuery):
    '''
    
    '''
    tg_id = callback.from_user.id

    user_db = await get_api(f'/game/by_user_id/{tg_id}')
    
    params={
        'telegram_user_id': tg_id
    }
    res = await delete_api(f'/game/delete/{user_db.id}', params=params)

    await callback.answer('')

    await callback.message.answer(
        'Вы покинули игру\n\n'
        'Результат матча:\n'
        f'Всего игр: {res.win_user_1 + res.win_user_2}\n'
        f'Ваших побед: {res.win_user_1 if res.your_id == res.id_user_1 else res.win_user_2}\n'
        f'Ваших поражений: {res.win_user_2 if res.your_id == res.id_user_1 else res.win_user_1}\n'
        f'Итог: {('вы проиграли' if res.id_user_1 < res.win_user_2 else 'вы выиграли') if res.your_id == res.id_user_1 else ('вы проиграли' if res.id_user_1 > res.win_user_2 else 'вы выиграли')}'
    )

    await send_to_user(
            bot=callback.bot,          # ← вот он, берётся из message
            user_telegram_id=tg_id,
            id_user_1=res.id_user_1,
            id_user_2=res.id_user_2,
            text='Ваш противник покинул игру\n\n'
            'Ваша статистика за эту игру:\n'
            f'Всего игр: {res.win_user_1 + res.win_user_2}\n'
            f'Ваших побед: {res.win_user_1 if res.your_id != res.id_user_1 else res.win_user_2}\n'
            f'Ваших поражений: {res.win_user_2 if res.your_id != res.id_user_1 else res.win_user_1}\n'
            f'Итог: {('вы проиграли' if res.id_user_1 < res.win_user_2 else 'вы выиграли') if res.your_id != res.id_user_1 else ('вы проиграли' if res.id_user_1 > res.win_user_2 else 'вы выиграли')}'
        )


@router.callback_query(F.data == 'next_game')
async def res_update_role(callback: CallbackQuery):
    '''
    
    '''
    await callback.answer('')
    tg_id = callback.from_user.id
    game_db = await get_api(f'/game/by_user_id/{tg_id}')

    
    params={
        'game_is_on': 'false' if game_db.game_is_on else 'true'
    }
    game_data = await post_api(f'/game/next/{game_db.id}', params=params)

    if game_data.game_is_on:
        await callback.message.answer(
            'Ожидайте второго игрока...',
            reply_markup=cancel_game_kb
        )

    else:
        await callback.message.answer(
            'Выберите фигуру:',
            reply_markup=game_kb
        )

        await send_to_user(
                bot=callback.bot,          # ← вот он, берётся из message
                user_telegram_id=tg_id,
                id_user_1=game_data.id_user_1,
                id_user_2=game_data.id_user_2,
                text='Выберите фигуру:',
                kb=game_kb
            )