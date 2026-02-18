from fastapi import APIRouter, Depends
from starlette import status
from app.schemas import CreateUser

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/all_users')
def get_all_users() -> dict:
    pass

@router.post('/create_user', status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser):
    return {'logs': f'{user.username} created'}