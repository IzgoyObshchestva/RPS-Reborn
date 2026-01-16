from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from ..models.user import User
from ..schemas.user import CreateUser, UpdateUser

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_tg_id(self, telegram_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()
    

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    
    async def create_user(self, user: CreateUser) -> User:
        db_user = User(
            telegram_id=user.telegram_id,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    

    async def delete_user(self, user_id: int) -> bool:
        result = await self.db.execute(
            delete(User).where(User.id == user_id).returning(User.id)
        )
        await self.db.commit()
        return result.scalar_one_or_none() is not None


    async def update_user(self, user_id: int, updat_data: UpdateUser) -> User:
        updat_dict = updat_data.model_dump(exclude_unset=True)

        if not updat_dict:
            return await self.get_user_by_id(user_id)
        
        stmt = update(User).where(User.id == user_id).values(**updat_dict)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_user_by_id(user_id)
    

    async def save_result_game(self, user_id: int, win: int, loss: int) -> User:
        stmt = update(User).where(User.id == user_id).values(win=User.win + win, loss=User.loss + loss).returning(User.id)

        await self.db.execute(stmt)

        await self.db.commit()

        return await self.get_user_by_id(user_id)