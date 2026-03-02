from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.backend.db_depends import get_db
from app.hotels.repo import HotelsRepo

router = APIRouter(prefix='/hotels', tags=['hotels'])


@router.get('/all')
async def get_all_hotels(db: Annotated[AsyncSession, Depends(get_db)]):
    return await HotelsRepo.get_all(db)


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int):
    hotel = await HotelsRepo.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='hotel not found')
    return hotel


@router.get('/search/{location}')
async def get_hotels_by_location(location: str = 'Алтай',
                                 date_from: date = '2023-12-12',
                                 date_to: date = '2023-12-13',):
    try:
        hotels = await HotelsRepo.search_hotels(location, date_from, date_to)
        return hotels
    except Exception as e:
        raise e

