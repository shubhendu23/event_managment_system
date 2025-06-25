from config.db_config import DBEngine
from config.logger import Logger
from models.events import Event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

logger = Logger().logger


class Events:
    def __init__(self):
        logger.info("Initializing Events service")
        self.local_sesion = sessionmaker(
                bind=DBEngine().engine,
                class_=AsyncSession,
                expire_on_commit=False)

    def create_event(self, event_data):
        pass

    async def get_events(self,):
        async with self.local_sesion() as session:
            events = await session.execute(select(Event))
            return events.scalars().all()

        