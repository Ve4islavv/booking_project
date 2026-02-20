from datetime import date
from typing import Optional
from fastapi import FastAPI, Query
from starlette import status
from app.schemas import SCreateBooking
from app.models import Booking, Users, Rooms, Hotels
from app.booking.routers import router as router_bookings
from app.users.routers import router as router_users
from app.rooms.routers import router as router_rooms
from app.hotels.routers import router as router_hotels

app = FastAPI()
app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_rooms)
app.include_router(router_hotels)


