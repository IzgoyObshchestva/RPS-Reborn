from typing import Annotated
from fastapi import HTTPException, Header, status
from ..core.config import settings

async def verify_bot_secret(x_bot_secret: Annotated[str, Header()]):
    if x_bot_secret != settings.BOT_API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid bot secret'
        )