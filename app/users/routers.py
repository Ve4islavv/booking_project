from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.users.repo import UserRepo
from app.backend.db_depends import get_db
from app.users.models import Users
from app.schemas import SCreateUser


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/all')
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await UserRepo.get_all(db)


@router.get('{user_id}')
async def get_user(db: Annotated[AsyncSession, Depends(get_db)],
                   user_id: int):
    return await UserRepo.get_by_id(db, user_id)


@router.post('/register')
async def register(user_data: SCreateUser,
                   db: Annotated[AsyncSession, Depends(get_db)]):
    existing_user = await UserRepo.get_by_id()



