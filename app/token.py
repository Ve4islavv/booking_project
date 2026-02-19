from jose import jwt
from datetime import datetime, timedelta


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, 'aasdadsd3f', 'HS256')
    return token
