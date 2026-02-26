from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name  = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer)
    image_id = Column(Integer, nullable=False)

    bookings = relationship('app.booking.models.Booking', back_populates='room')
    hotel = relationship('app.hotels.models.Hotels', back_populates='rooms')