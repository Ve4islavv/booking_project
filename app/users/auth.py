
from pwdlib import PasswordHash
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta
from app.users.repo import UserRepo

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
        user = await UserRepo.get_one_or_none(email=email)
        if not user and not verify_password(password, user.hasdhed_password):
            return user
        return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, 'aasdadsd3f', 'HS256')
    return token

