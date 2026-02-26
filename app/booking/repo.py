from datetime import date
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated
from starlette import status
from sqlalchemy import select, and_, or_, func, insert, delete

from app.backend.db import async_session_maker
from app.repo.base import BaseRepo
from app.booking.models import Booking
from app.hotels.rooms.models import Rooms
from app.users.dependencies import get_current_user
from app.users.models import Users


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
            await session.execute(insert(Booking).values(room_id=room_id,
                                                         user_id=user_id,
                                                         date_from=date_from,
                                                         date_to=date_to,
                                                         price=price).returning(Booking))
            await session.commit()

    @classmethod
    async def get_user_bookings(cls, user_id: int):
        query = (select(cls.model.room_id,
                       cls.model.user_id,
                       cls.model.date_from,
                       cls.model.date_to,
                       cls.model.price,
                       cls.model.total_days,
                       cls.model.total_cost,
                       Rooms.image_id,
                       Rooms.name,
                       Rooms.description,
                       Rooms.services
                       )
                .join(Rooms, Rooms.id == Booking.room_id)
                 .where(Booking.user_id == user_id)
                 .order_by(Booking.date_from.desc())
                 )
        async with async_session_maker() as session:
            result = await session.execute(query)
            bookings = result.all()

            if not bookings:
                print(f"✅ Бронирований не найдено")
                return []

            print(f"✅ Найдено бронирований: {len(bookings)}")

            bookings_list = []
            for booking in bookings:
                services = booking[10]
                if services is None:
                    services = []
                elif not isinstance(services, list):
                    if isinstance(services, dict):
                        services = list(services.values()) if services else []
                    else:
                        services = [str(services)]

                bookings_list.append({
                    "room_id": booking[0],
                    "user_id": booking[1],
                    "date_from": booking[2],
                    "date_to": booking[3],
                    "price": booking[4],
                    "total_cost": booking[5],
                    "total_days": booking[6],
                    "image_id": booking[7],
                    "name": booking[8],
                    "description": booking[9],
                    "services": services
                })
                print(f"  • {booking[8]}: {booking[5]} руб, {booking[6]} дней")

            return bookings_list


    @classmethod
    async def delete_booking(cls, booking_id: int,
                             user_id: int):
        async with async_session_maker() as session:
            query = delete(Booking).where(Booking.id == booking_id,
                                          Booking.user_id == user_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                return False
            return True


