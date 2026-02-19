from app.repo.base import BaseRepo
from app.booking.models import Booking


class BookingClass(BaseRepo):
    model = Booking