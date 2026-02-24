from typing import Annotated
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db_depends import get_db
from app.core.config import settings
from app.users.repo import UserRepo


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZE,
                            detail='token not found in cookies')
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)],
                           db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError as e:
        raise e
    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='token time out')
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='user_id not found')
    user = await UserRepo.get_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User not found')
    return user

