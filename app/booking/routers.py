from datetime import date

from fastapi import APIRouter, Path, Depends
from typing import Annotated


from sqlalchemy import select, update, delete, insert
from starlette import status

from app.schemas import SCreateBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

from app.backend.db_depends import get_db
from app.booking.repo import BookingRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.booking.models import Booking

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('/all')
async def get_all_bookings(db: Annotated[AsyncSession, Depends(get_db)]):
    return await BookingRepo.get_all(db)


@router.get('/users_booking')
async def get_user_bookings(db: Annotated[AsyncSession, Depends(get_db)],
                           user: Annotated[Users, Depends(get_current_user)]):

    return await BookingRepo.get_all(db, user.id)

@router.get('/{booking_id}')
async def get_booking(db: Annotated[AsyncSession, Depends(get_db)],
                      booking_id: Annotated[int, Path(...)]):
    return await BookingRepo.get_by_id(db=db, id=booking_id)


@router.post('/create_booking', status_code=status.HTTP_201_CREATED)
async def add_booking(room_id: int,
                      date_from: date,
                      date_to: date,
                      user: Users = Depends(get_current_user)):
    await BookingRepo.add(user_id=user.id,
                           room_id=room_id,
                           date_from=date_from,
                           date_to=date_to,
                           )
    return {'message': 'Rooms booked'}





