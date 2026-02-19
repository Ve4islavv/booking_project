from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from app.backend.db import Base
from sqlalchemy.orm import relationship





class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
    total_days = Column(Integer, Computed('(date_to - date_from)'))
    room = relationship('app.rooms.models.Rooms', back_populates='bookings')
    user = relationship('app.users.models.Users', back_populates='bookings')

