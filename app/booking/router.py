from fastapi import APIRouter, Path, Depends
from typing import Annotated


from sqlalchemy import select, update, delete, insert

from app.backend.db_depends import get_db
from app.booking.repo import BookingClass
from sqlalchemy.ext.asyncio import AsyncSession
from app.booking.models import Booking

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('/all')
async def get_all_bookings(db: Annotated[AsyncSession, Depends(get_db)]):
    return await BookingClass.get_all(db)


@router.get('/{booking_id}')
def get_booking(booking_id: Annotated[int, Path(...)]):
    pass

