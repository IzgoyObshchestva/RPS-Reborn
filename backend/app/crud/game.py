from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, or_

from ..models.game import Game
from ..schemas.game import CreateGame, UpdateGame

class GameRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_game_by_id(self, game_id: int) -> Game | None:
        '''
        Возвращает игру по её id в БД.

        Args:
            game_id (int): id игры.

        Returns:
            Game | None
        '''
        result = await self.db.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()
    

    async def get_game_by_invitation_code(self, invitation_code: str) -> Game | None:
        '''
        Возвращает игру по её invitation_code в БД.

        Args:
            invitation_code (str): invitation_code игры.

        Returns:
            Game | None
        '''
        result = await self.db.execute(select(Game).where(Game.invitation_code == invitation_code))
        return result.scalar_one_or_none()
    

    async def get_game_by_user_id(self, user_id: int) -> Game | None:
        '''
        Возвращает игру по id пользователя из БД.

        Args:
            user_id (int): id пользователя.

        Returns:
            Game | None
        '''
        result = await self.db.execute(
            select(Game)
            .where(or_(
                    Game.id_user_1 == user_id,
                    Game.id_user_2 == user_id
                )
            ))
        return result.scalar_one_or_none()
    
    
    async def create_game(self, game: CreateGame) -> Game:
        '''
        Создание игры в БД.

        Args:
            game (CreateGame): всё необходимое для создания игры.

        Returns:
            Game | None
        '''
        db_user = Game(
            id_user_1=game.id_user_1,
            invitation_code=game.invitation_code
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    

    async def delete_game(self, game_id: int) -> Game | None:
        '''
        Удаление игры из БД.

        Args:
            game_id (int): id игры.

        Returns:
            Game | None
        '''
        game_db = await self.get_game_by_id(game_id)

        result = await self.db.execute(
            delete(Game).where(Game.id == game_id).returning(Game.id)
        )
        await self.db.commit()

        if result.scalar_one_or_none() is not None:
            return game_db
        
        return None


    async def update_game(self, game_id: int, updat_data: UpdateGame) -> Game:
        '''
        Изменение записи игры в БД.

        Args:
            game_id (int): id игры.
            updat_data (UpdateGame): паля которые нужно изменить.

        Returns:
            Game
        '''
        updat_dict = updat_data.model_dump(exclude_unset=True)

        if not updat_dict:
            return await self.get_game_by_id(game_id)
        
        stmt = update(Game).where(Game.id == game_id).values(**updat_dict)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_game_by_id(game_id)