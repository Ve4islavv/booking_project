from fastapi import APIRouter, Path, Depends
from typing import Annotated


from sqlalchemy import select, update, delete, insert
from app.backend.db_depends import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.booking.models import Booking

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_all_bookings(db: Annotated[AsyncSession, Depends(get_db)],
                           user_id: int):
    bookings = await db.scalars(select(Booking).where(Booking.user_id == user_id))
    return bookings.all()


@router.get('/{booking_id}')
def get_booking(booking_id: Annotated[int, Path(...)]):
    pass