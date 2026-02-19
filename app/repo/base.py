from fastapi import HTTPException
from pydantic.v1 import EmailStr

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class BaseRepo:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession, user_id: int = False):
        if user_id:
            result = await db.scalars(select(cls.model).where(cls.model.user_id == user_id))
            return result.all()
        bookings = await db.scalars(select(cls.model))
        return bookings.all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        result = await db.scalar(select(cls.model).where(cls.model.id == id))
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result







