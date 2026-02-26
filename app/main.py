from fastapi import FastAPI
from app.booking.routers import router as router_bookings
from app.users.routers import router as router_users

from app.hotels.rooms.routers import router as router_hotels

app = FastAPI()
app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)


