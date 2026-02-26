from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.backend.db import Base

class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    rooms = relationship('app.hotels.rooms.models.Rooms', back_populates='hotel')