from fastapi import FastAPI
from contextlib import  asynccontextmanager

from .db.init_db import init_db
from .db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    try:
        yield
    finally:
        # ===== SHUTDOWN =====
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def zxc():
    return {'message': 'zxcqwe'}