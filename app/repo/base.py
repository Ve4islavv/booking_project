from fastapi import HTTPException
from pydantic.v1 import EmailStr
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.backend.db import async_session_maker


class BaseRepo:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession, user_id: int | None = None):
        if user_id is not None:
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


    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.scalar(query)
            return result


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, email: EmailStr):
        async with async_session_maker() as session:
            await session.execute(delete(cls.model).where(cls.model.email == email))
            await session.commit()





