from fastapi import APIRouter, Depends, HTTPException, Response, Path
from pydantic import EmailStr
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
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
async def register_user(user_data: SCreateUser):
    existing_user = await UserRepo.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Email already used')
    hashed_password = get_password_hash(user_data.password)
    await UserRepo.add(email=user_data.email, hashed_password=hashed_password)
    return {'status': status.HTTP_201_CREATED,
            'transaction': 'user created'}


@router.delete('/delete/{email}')
async def delete_user(email: Annotated[EmailStr, Path(...)],
                      password: str):
    existing_user = await UserRepo.get_one_or_none(email=email)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='password invalid')
    await UserRepo.delete(email=email)
    return {'status': status.HTTP_200_OK,
            'transaction': 'user deleted'}


@router.post('/login')
async def login_user(response: Response, user_data: SCreateUser):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'message': 'success login'}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def info_about_user(user: Annotated[Users, Depends(get_current_user)]):
    return user







