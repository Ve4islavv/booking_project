from pydantic import BaseModel, EmailStr
from datetime import date


class SCreateBooking(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

    class Config:
        from_attributes = True

class SCreateUser(BaseModel):
    email: EmailStr
    password: str