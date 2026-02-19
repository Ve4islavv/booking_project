from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.base import BaseRepo
from app.booking.models import Booking



class BookingRepo(BaseRepo):
    model = Booking
