from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.rooms.repo import RoomsRepo

router = APIRouter(prefix='/rooms', tags=['rooms'])


@router.get('/all')
async def get_all_rooms(db: Annotated[AsyncSession, Depends(get_db)]):
    return await RoomsRepo.get_all(db)


@router.get('/{room_id}')
async def get_room(db: Annotated[AsyncSession, Depends(get_db)],
                   room_id: Annotated[int, Path(...)]):
    return await RoomsRepo.get_by_id(db, room_id)