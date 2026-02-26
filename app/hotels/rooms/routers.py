from datetime import date

from fastapi import Depends, Path, HTTPException
from typing import Annotated
from app.hotels.repo import HotelsRepo
from app.hotels.rooms.repo import RoomsRepo
from app.hotels.routers import router
from starlette import status
from app.schemas import SCreateRoom


@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id: int,
                        date_from: date,
                        date_to: date):
    return await RoomsRepo.get_rooms_in_hotel(hotel_id,
                                              date_from,
                                              date_to)


@router.get('/hotel_name/{room_id}')
async def get_room(room_id: Annotated[int, Path(...)]):
    return await RoomsRepo.get_one_or_none(id=room_id)


@router.post('/{hotel_id}/create_room', status_code=status.HTTP_201_CREATED)
async def create_new_room(room: SCreateRoom,
                          hotel_id: int):
    hotel = await HotelsRepo.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Hotel not found')
    await RoomsRepo.add(hotel_id=hotel_id,
                        name=room.name,
                        description=room.description,
                        price=room.price,
                        services=room.services,
                        quantity=room.quantity,
                        image_id=room.image_id)



