from config.db_config import DBEngine
from config.logger import Logger
from models.attendees import Attendee  
from models.events import Event  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func

class Attendees:
    def __init__(self):
        self.local_session =  sessionmaker(
            bind=DBEngine().get_engine(),
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def register(self, event_id, attendee_data):
        """
        Registers a new attendee for a specific event.
        
        :param event_id: ID of the event for which the attendee is being registered.
        :param attendee_data: Dictionary containing attendee details (name, email, contact_number).
        :return: The newly created Attendee object.
        """
        
        async with self.local_session() as session:
            max_capacity = await session.execute(
                select(Event.max_capacity).where(Event.id == event_id)
            )
            max_capacity = max_capacity.scalar_one() or 0
            
            attendes_count = await session.execute(
                select(func.count(Attendee.id)).where(Attendee.event_id == event_id)
            )

            unique_email = await session.execute(
                select(func.count(Attendee.id)).where(
                    Attendee.event_id == event_id,
                    Attendee.email == attendee_data.email
                ))
            if unique_email.scalar_one() > 0:
                raise ValueError("Email already registered for this event.")
            attendes_count = attendes_count.scalar_one() or 0
            if attendes_count >= max_capacity:
                raise ValueError("Event is fully booked. Cannot register more attendees.")
            new_attendee = Attendee(
                name=attendee_data.name,
                email=attendee_data.email,
                contact_number=attendee_data.contact_number,
                event_id=event_id
            )
            session.add(new_attendee)
            await session.commit()
            return new_attendee
        

    async def get_attendees(self, event_id, limit: int = 10, offset: int = 0):
        async with self.local_session() as session:
            attendees = await session.execute(
            select(Attendee).where(Attendee.event_id == event_id).limit(limit).offset(offset)
            )
            return attendees.scalars().all()


        
