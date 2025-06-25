from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Event(AsyncAttrs,Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<Event(name={self.name}, description={self.description}, "
                f"start_datetime={self.strat_datetime}, end_datetime={self.end_datetime}, "
                f"location={self.location}, max_capacity={self.max_capacity})>")