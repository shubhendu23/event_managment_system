# DTOs
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class EventCreateDTO(BaseModel):
    name: str
    start_datetime: str
    end_datetime: Optional[str] = None
    location: str
    max_capacity: int
    description: Optional[str] = None
    timezone: Optional[str] = None

    class Config:
        from_attributes = True

class EventDTO(EventCreateDTO):
    id: int

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

    @field_validator("attendee_email")
    def validate_email(cls, value: str) -> str:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        return value.lower()

class AttendeeDTO(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    contact_number: Optional[str] = None

    class Config:
        from_attributes = True

