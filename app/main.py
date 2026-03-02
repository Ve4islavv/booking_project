from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.booking.routers import router as router_bookings
from app.users.routers import router as router_users
from app.hotels.rooms.routers import router as router_rooms
from app.hotels.routers import router as router_hotels
from app.pages.routers import router as router_page
from app.images.router import router as router_image
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_page)
app.include_router((router_image))
app.mount('/static', StaticFiles(directory='app/static'), 'static')

origins = ['http://localhost:3000']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
                   allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                                  'Access-Control-Allow-Origin',
                                  'Authorization'])




