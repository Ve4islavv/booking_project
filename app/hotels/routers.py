from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

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