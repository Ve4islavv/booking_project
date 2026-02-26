from datetime import date
from fastapi import HTTPException
from sqlalchemy import select, and_, func
from app.backend.db import async_session_maker
from app.booking.models import Booking
from app.hotels.repo import HotelsRepo
from app.repo.base import BaseRepo
from app.hotels.rooms.models import Rooms
from starlette import status


class RoomsRepo(BaseRepo):
    model = Rooms

    @classmethod
    async def get_rooms_in_hotel(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        days_count = (date_to - date_from).days
        if days_count <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Некорректный интервал дат'
            )

        hotel = await HotelsRepo.get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Отель не найден'
            )

        booked_counts = (
            select(
                Booking.room_id,
                func.count(Booking.id).label('booked_count')
            )
            .join(Rooms, Rooms.id == Booking.room_id)
            .where(
                and_(
                    Rooms.hotel_id == hotel_id,
                    Booking.date_from <= date_to,
                    Booking.date_to >= date_from
                )
            )
            .group_by(Booking.room_id)
            .subquery()
        )

        query = (
            select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * days_count).label('total_cost'),
                (Rooms.quantity - func.coalesce(booked_counts.c.booked_count, 0)).label('rooms_left')
            )
            .outerjoin(
                booked_counts,
                booked_counts.c.room_id == Rooms.id
            )
            .where(Rooms.hotel_id == hotel_id)
            .group_by(Rooms.id, booked_counts.c.booked_count)
            .order_by(Rooms.id)
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            rooms = result.all()

            rooms_list = []
            for room in rooms:
                rooms_left = room[9]  # rooms_left
                print(f"  • {room[2]}: всего {room[6]}, свободно {rooms_left}")

                rooms_list.append({
                    "id": room[0],
                    "hotel_id": room[1],
                    "name": room[2],
                    "description": room[3],
                    "services": room[4],
                    "price": room[5],
                    "quantity": room[6],
                    "image_id": room[7],
                    "total_cost": room[8],
                    "rooms_left": max(0, rooms_left)
                })

            return rooms_list