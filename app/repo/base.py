from app.backend.db import async_session_maker
from sqlalchemy import select
from app.backend.db_depends import get_db
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepo:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession):
        bookings = await db.scalars(select(cls.model))
        return bookings.all()


    @classmethod
    async def get_user_booking(cls, user_id: int):
        pass