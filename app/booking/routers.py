from datetime import date
from fastapi import APIRouter, Path, Depends, Request, HTTPException
from typing import Annotated
from sqlalchemy import select, update, delete, insert
from starlette import status
from app.schemas import SCreateBooking, SBookingResponse
from app.users.dependencies import get_current_user, get_token
from app.users.models import Users
from app.backend.db_depends import get_db
from app.booking.repo import BookingRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.booking.models import Booking

router = APIRouter(prefix='/bookings', tags=['Бронирования'])



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


@router.delete('/{booking_id}')
async def delete_booking(booking_id: Annotated[int, Path(..., description="ID бронирования для удаления", ge=1)],
                         user: Annotated[Users, Depends(get_current_user)]):
    result = await BookingRepo.delete_booking(user_id=user.id, booking_id=booking_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='booking not found or user dont has permission')
    return None






