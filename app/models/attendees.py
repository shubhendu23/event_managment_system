from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Attendee(AsyncAttrs,Base):
    __tablename__ = 'attendees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    event_id = Column(Integer, nullable=False)
    contact_number = Column(String(15), nullable=True)

    def __repr__(self):
        return f"<Attendee(name={self.name}, email={self.email}, event_id={self.event_id}), contact_number={self.contact_number})>"