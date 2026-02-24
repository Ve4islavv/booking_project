from datetime import date
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select, and_, or_, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db import engine, async_session_maker
from app.repo.base import BaseRepo
from app.booking.models import Booking
from app.rooms.models import Rooms


class BookingRepo(BaseRepo):
    model = Booking

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM booking
            WHERE room_id = 1 and
            ((date_from >= '2023-06-15' AND date_from <= '2023-06-30')
                OR (date_from <= '2023-06-15' AND date_to <= '2023-06-30'))
        )
        select rooms.quantity - COUNT(booked_rooms.room_id) from rooms
        left join booked_rooms
            on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        group by rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                Booking.room_id == room_id,
                    (
                        or_(
                            and_(Booking.date_from >= date_from, Booking.date_from <= date_to
                        ), and_(Booking.date_from <= date_from, Booking.date_to > date_from)

                    ))
                )
            ).cte('booked_rooms')
            free_rooms = await session.scalar(select(Rooms.quantity - func.coalesce(func.count(booked_rooms.c.room_id)
                               , 0)).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(Rooms.quantity, booked_rooms.c.room_id))
            print(free_rooms)
            if free_rooms is None or free_rooms <= 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='rooms busy in this date interval')


            price = await session.scalar((select(Rooms.price).where(Rooms.id == room_id)))
            new_booking = await session.execute(insert(Booking).values(room_id=room_id,
                                                         user_id=user_id,
                                                         date_from=date_from,
                                                         date_to=date_to,
                                                         price=price).returning(Booking))
            await session.commit()

