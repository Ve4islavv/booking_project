from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.backend.db_depends import get_db
from app.hotels.repo import HotelsRepo

router = APIRouter(prefix='/hotels', tags=['hotels'])


@router.get('/all')
async def get_all_hotels(db: Annotated[AsyncSession, Depends(get_db)]):
    return await HotelsRepo.get_all(db)


@router.get('/{hotel_id}')
async def get_hotel(database: Annotated[AsyncSession, Depends(get_db)],
                    hotel_id: Annotated[int, Path(...)]):
    return await HotelsRepo.get_by_id(db=database, id=hotel_id)


@router.get('/search/{location}')
async def get_hotels_by_location(location: str,
                                 date_from: date,
                                 date_to: date):
    try:
        hotels = await HotelsRepo.search_hotels(location, date_from, date_to)
        return hotels
    except Exception as e:
        raise e

