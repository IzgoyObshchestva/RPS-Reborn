import asyncio
import uvicorn

from bot.main import run_bot
from backend.app.main import app as fastapi_app

async def run_api():
    config = uvicorn.Config(fastapi_app, reload=True, use_colors=False)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    api_task = asyncio.create_task(run_api())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(api_task, bot_task)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('🛑 Остановка проекта...')