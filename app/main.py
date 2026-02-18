from datetime import date
from typing import Optional
from fastapi import FastAPI, Query
from starlette import status
from app.schemas import CreateBooking
from app.routers.users import router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/hotels')
def get_hotels(location: str,
               date_from: date,
               date_to: date,
               has_spa: Optional[bool] = None,
               stars: int = Query(default=None, ge=1, le=5)) -> str:
    return f'all hotels {date_from}'

@app.post('/booking', status_code=status.HTTP_201_CREATED, response_model=dict)
def add_booking(booking: CreateBooking):
    return {'user': booking.user_id,
            'transaction': f'{booking.room_id} reserved'}
