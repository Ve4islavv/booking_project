from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    bookings = relationship('app.booking.models.Booking', back_populates='user')

