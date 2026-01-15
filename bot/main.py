from aiogram import Bot, Dispatcher
from .handlers.basic import router as basic_router
from .handlers.game import router as game_router

from .core.config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def run_bot():
    dp.include_routers(
        basic_router,
        game_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)