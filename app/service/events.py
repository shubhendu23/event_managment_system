from config.db_config import DBEngine
from config.logger import Logger
from models.events import Event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from datetime import datetime

logger = Logger().logger


class Events:
    def __init__(self):
        logger.info("Initializing Events service")
        self.local_sesion = sessionmaker(
                bind=DBEngine().engine,
                class_=AsyncSession,
                expire_on_commit=False)

    async def create_event(self, event_data):
        async with self.local_sesion() as session:
            new_event = Event(
                name=event_data.name,
                description=event_data.description,
                start_datetime=datetime.strptime(event_data.start_datetime, "%Y-%m-%d %H:%M:%S"),
                end_datetime=datetime.strptime(event_data.end_datetime,"%Y-%m-%d %H:%M:%S"),
                location=event_data.location,
                max_capacity=event_data.max_capacity
            )
            session.add(new_event)
            await session.commit()
            return new_event

    async def get_events(self,):
        async with self.local_sesion() as session:
            events = await session.execute(select(Event))
            return events.scalars().all()

        