from fastapi.params import Query
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List


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

class SCreateRoom(BaseModel):
    name: str
    description: str
    price: int = Query(gt=0)
    services: dict
    quantity: int = Query(gt=0)
    image_id: int


class SBookingResponse(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: Optional[int]
    name: str
    description: Optional[str]
    services: List[str] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True