from fastapi import APIRouter, Path, Depends
from typing import Annotated


from sqlalchemy import select, update, delete, insert
from app.users.routers import get_user
from app.backend.db_depends import get_db
from app.booking.repo import BookingRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.booking.models import Booking

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('/all')
async def get_all_bookings(db: Annotated[AsyncSession, Depends(get_db)]):
    return await BookingRepo.get_all(db)


@router.get('/{booking_id}')
async def get_booking(db: Annotated[AsyncSession, Depends(get_db)],
                      booking_id: Annotated[int, Path(...)]):
    return await BookingRepo.get_by_id(db=db, id=booking_id)


@router.get('/{user_id}')
async def get_user_bookings(db: Annotated[AsyncSession, Depends(get_db)],
                           user_id: int):
    await get_user(db, user_id)
    return await BookingRepo.get_all(db, user_id)

