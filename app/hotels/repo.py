from sqlalchemy import select, func, and_, or_

from app.backend.db import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.booking.models import Booking
from datetime import date
from app.repo.base import BaseRepo


class HotelsRepo(BaseRepo):
    model = Hotels

    @classmethod
    async def search_hotels(cls,
                            location: str,
                            date_from: date,
                            date_to: date):
        booked_subquery = (
            select(Booking.room_id)
            .where(
                and_(
                    Booking.date_from <= date_to,
                    Booking.date_to >= date_from
                )
            )
        .distinct()
        .subquery()
        )

        query = (
            select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.image_id,
                func.count(Rooms.id).label('rooms_quantity'),
                (func.count(Rooms.id) -
                 func.count(booked_subquery.c.room_id)).label('rooms_left')
            )
            .join(Rooms, Rooms.hotel_id == Hotels.id)
            .outerjoin(
                booked_subquery,
                booked_subquery.c.room_id == Rooms.id
            )
            .where(Hotels.location.ilike(f'%{location}%'))
            .group_by(Hotels.id)
            .having(
                func.count(Rooms.id) - func.count(booked_subquery.c.room_id) > 0
            )
        )
        async with async_session_maker() as session:
            result = await session.execute(query)
            hotels = []
            for row in result:
                hotels.append({
                    "id": row[0],
                    "name": row[1],
                    "location": row[2],
                    "services": row[3],
                    "image_id": row[4],
                    "rooms_quantity": row[5],
                    "rooms_left": row[6]
                })

            return hotels