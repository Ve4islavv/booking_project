from pydantic import BaseModel
from datetime import date


class CreateBooking(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    username: str
    password: str