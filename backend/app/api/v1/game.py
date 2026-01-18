from fastapi import APIRouter, Depends, HTTPException, status


from ...schemas.user import CreateUser, UserResponse, UpdateUser
from ...crud.user import UserRepository

from ...schemas.game import CreateGame, GameResponse, UpdateGame
from ...crud.game import GameRepository

from ...db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import verify_bot_secret, get_user_id_in_db
from ...utils.func import generate_invite_code, result_game
from ...utils.generator_img import async_image_generator, delete_file

router = APIRouter(dependencies=[Depends(verify_bot_secret)])


@router.post('/game/create', status_code=status.HTTP_201_CREATED)
async def create_game(
    user_id: int,
    # game_data: CreateGame,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Создание игры
    
    :param user_id: Описание
    :type user_id: int
    :param db: Описание
    :type db: AsyncSession
    '''
    repo = GameRepository(db)

    res = await repo.get_game_by_user_id(user_id)

    if res:
        # Если пользователь уже состоит в какой-либо игре, то ему нельзя начать другую
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть игра')

    game_data = CreateGame(
        id_user_1=user_id,
        invitation_code=generate_invite_code()
    )

    game_db = await repo.create_game(game_data)

    return {'invitation_code': game_db.invitation_code}


@router.patch('/game/join/{game_id}')
async def join_game(
    game_id: int,
    game_data: UpdateGame,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Пользователь присоеденяется к игре
    
    :param game_id: Описание
    :type game_id: int
    :param game_data: Описание
    :type game_data: UpdateGame
    :param db: Описание
    :type db: AsyncSession
    '''
    repo = GameRepository(db)

    res = await repo.get_game_by_user_id(game_data.id_user_2)

    if res:
        # Если пользователь уже состоит в какой-либо игре, то ему нельзя начать другую
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть игра')
    
    game_db = await repo.update_game(game_id, game_data)

    return {
        'id': game_db.id,
        'id_user_1': game_db.id_user_1,
        'id_user_2': game_db.id_user_2,
        'last_figure_1': game_db.last_figure_1,
        'last_figure_2': game_db.last_figure_2,
        'win_user_1': game_db.win_user_1,
        'win_user_2': game_db.win_user_2,
        'invitation_code': game_db.invitation_code,
        'game_is_on': game_db.game_is_on
    }


@router.post('/game/next/{game_id}')
async def next_game(
    game_id: int,
    game_is_on: bool,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Пользователь присоеденяется к игре
    
    :param game_id: Описание
    :type game_id: int
    :param game_data: Описание
    :type game_data: UpdateGame
    :param db: Описание
    :type db: AsyncSession
    '''
    repo = GameRepository(db)

    game_data = UpdateGame(
        game_is_on=game_is_on
    )
    
    game_db = await repo.update_game(game_id, game_data)

    return {
        'id': game_db.id,
        'id_user_1': game_db.id_user_1,
        'id_user_2': game_db.id_user_2,
        'last_figure_1': game_db.last_figure_1,
        'last_figure_2': game_db.last_figure_2,
        'win_user_1': game_db.win_user_1,
        'win_user_2': game_db.win_user_2,
        'invitation_code': game_db.invitation_code,
        'game_is_on': game_db.game_is_on
    }


@router.patch('/game/figure/')
async def figure_game(
    user_tg_id: int,
    figure: str,
    # game_data: UpdateGame,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Пользователь отправляет выбранную фигуру
    
    :param game_id: Описание
    :type game_id: int
    :param game_data: Описание
    :type game_data: UpdateGame
    :param db: Описание
    :type db: AsyncSession
    '''
    repo_user = UserRepository(db)

    user_db = await repo_user.get_user_by_tg_id(user_tg_id)

    repo = GameRepository(db)

    res = await repo.get_game_by_user_id(user_db.id)

    if user_db.id == res.id_user_1:
        game_data = UpdateGame(
            last_figure_1=figure
        )
    else:
        game_data = UpdateGame(
            last_figure_2=figure
        )

    # if res:
    #     # Если пользователь уже состоит в какой-либо игре, то ему нельзя начать другую
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть игра')
    
    game_db = await repo.update_game(res.id, game_data)

    return {
        'id': game_db.id,
        'id_user_1': game_db.id_user_1,
        'id_user_2': game_db.id_user_2,
        'last_figure_1': game_db.last_figure_1,
        'last_figure_2': game_db.last_figure_2,
        'win_user_1': game_db.win_user_1,
        'win_user_2': game_db.win_user_2,
        'invitation_code': game_db.invitation_code,
        'game_is_on': game_db.game_is_on
    }


@router.post('/game/result_game/{game_id}')
async def get_result_game(
    game_id: int,
    your_id: int = Depends(get_user_id_in_db),
    db: AsyncSession = Depends(get_db),
):
    '''
    Возвращяет итоги игры
    '''
    repo = GameRepository(db)

    game_db = await repo.get_game_by_id(game_id)

    if game_db.img_name:
        delete_file(game_db.img_name)

    img_name = await async_image_generator(game_db.last_figure_1, game_db.last_figure_2)

    if game_db.last_figure_1 == game_db.last_figure_2:
        # Ничья
        game_data = UpdateGame(
            last_figure_1=None,
            last_figure_2=None,
            img_name=img_name
        )
        res_game = await repo.update_game(game_id, game_data)

        return {
            'win_id_user': None,
            'your_id': your_id,
            'id': res_game.id,
            'id_user_1': res_game.id_user_1,
            'id_user_2': res_game.id_user_2,
            'img': res_game.img_name,
            'win_user_1': res_game.win_user_1,
            'win_user_2': res_game.win_user_2,
        }


    res = result_game(game_db.last_figure_1, game_db.last_figure_2)

    if res:
        game_data = UpdateGame(
            win_user_1=game_db.win_user_1+1,
            last_figure_1=None,
            last_figure_2=None,
            img_name=img_name
        )
        win_id_user = game_db.id_user_1
    else:
        game_data = UpdateGame(
            win_user_2=game_db.win_user_2+1,
            last_figure_1=None,
            last_figure_2=None,
            img_name=img_name
        )
        win_id_user = game_db.id_user_2

    res_game = await repo.update_game(game_id, game_data)

    return {
        'win_id_user': win_id_user,
        'your_id': your_id,
        'id': res_game.id,
        'id_user_1': res_game.id_user_1,
        'id_user_2': res_game.id_user_2,
        'img': res_game.img_name,
        'win_user_1': res_game.win_user_1,
        'win_user_2': res_game.win_user_2,
    }




@router.patch('/game/update/{game_id}')
async def update_game(
    game_id: int,
    game_data: UpdateGame,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Именение игры
    
    :param game_id: Описание
    :type game_id: int
    :param game_data: Описание
    :type game_data: UpdateGame
    :param db: Описание
    :type db: AsyncSession
    '''
    pass


@router.delete('/game/delete/{game_id}')
async def delete_game(
    game_id: int,
    telegram_user_id: int,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Удаления игры
    
    :param game_id: Описание
    :type game_id: int
    :param db: Описание
    :type db: AsyncSession
    '''
    repo = GameRepository(db)

    res = await repo.delete_game(game_id)

    if res:
        user_repo = UserRepository(db)

        if res.img_name:
            delete_file(res.img_name)

        user_1 = await user_repo.save_result_game(res.id_user_1, res.win_user_1, res.win_user_2)
        user_2 = await user_repo.save_result_game(res.id_user_2, res.win_user_2, res.win_user_1)

        if telegram_user_id == user_1.telegram_id:
            your_id_in_db = user_1.id
        else:
            your_id_in_db = user_2.id

        return {
            'action': True,
            'id_user_1': res.id_user_1,
            'id_user_2': res.id_user_2,
            'win_user_1': res.win_user_1,
            'win_user_2': res.win_user_2,
            'your_id': your_id_in_db
        }


@router.get('/game/by_user_id/{tg_id}')
async def get_game_by_user_id(
    tg_id: int,
    db: AsyncSession = Depends(get_db),
    current_bot: None = Depends(verify_bot_secret)
):
    '''
    Поиск игры по telegram id пользователя
    
    :param tg_id: Описание
    :type tg_id: int
    :param db: Описание
    :type db: AsyncSession
    :param current_bot: Описание
    :type current_bot: None
    '''
    user_repo = UserRepository(db)

    user_db = await user_repo.get_user_by_tg_id(tg_id)

    repo = GameRepository(db)

    game_db = await repo.get_game_by_user_id(user_db.id)

    return {
        'id': game_db.id,
        'id_user_1': game_db.id_user_1,
        'id_user_2': game_db.id_user_2,
        'last_figure_1': game_db.last_figure_1,
        'last_figure_2': game_db.last_figure_2,
        'win_user_1': game_db.win_user_1,
        'win_user_2': game_db.win_user_2,
        'invitation_code': game_db.invitation_code,
        'game_is_on': game_db.game_is_on
    }


@router.get('/game/invitation/{invitation_code}')
async def get_game_by_invitation_code(
    invitation_code: str,
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    '''
    Поиск игры по invitation code
    '''
    repo = GameRepository(db)

    game_db = await repo.get_game_by_invitation_code(invitation_code)

    if game_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Не верный код')
    elif game_db.id_user_2 != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не можете присоединиться. Пользователи уже играют')

    return {
        'id': game_db.id,
        'id_user_1': game_db.id_user_1,
        'id_user_2': game_db.id_user_2,
        'last_figure_1': game_db.last_figure_1,
        'last_figure_2': game_db.last_figure_2,
        'win_user_1': game_db.win_user_1,
        'win_user_2': game_db.win_user_2,
        'invitation_code': game_db.invitation_code,
        'game_is_on': game_db.game_is_on
    }


@router.get('/game/{game_id}')
async def get_game_by_id(
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    pass


@router.get('/game/')
async def get_game_all(
    db: AsyncSession = Depends(get_db),
    # current_bot: None = Depends(verify_bot_secret)
):
    pass