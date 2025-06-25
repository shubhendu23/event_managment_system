# DTOs
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class EventCreateDTO(BaseModel):
    name: str
    date: str
    location: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class EventDTO(BaseModel):
    id: int
    start_datetime: str
    end_datetime: Optional[str] = None
    max_capacity: int
    name: str
    location: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator("start_datetime", "end_datetime",mode="before")
    def convert_datetime(cls, value: datetime) -> str:
        return datetime.strftime(value, "%Y-%m-%dT%H:%M:%S") if value else value
    
class RegisterDTO(BaseModel):
    attendee_name: str
    attendee_email: str
    contact_number: Optional[str] = None
    
    class Config:
        from_attributes = True

class AttendeeDTO(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    contact_number: Optional[str] = None

    class Config:
        from_attributes = True

