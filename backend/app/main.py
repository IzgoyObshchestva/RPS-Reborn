from fastapi import FastAPI
from contextlib import  asynccontextmanager

from .db.init_db import init_db
from .db.session import engine

from .api.v1.user import router as user_router_v1
from .api.v1.game import router as game_router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    try:
        yield
    finally:
        # ===== SHUTDOWN =====
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router_v1, prefix='/api/v1', tags=['User'])
app.include_router(game_router_v1, prefix='/api/v1', tags=['Game'])

@app.get('/')
async def zxc():
    return {'message': 'zxcqwe'}