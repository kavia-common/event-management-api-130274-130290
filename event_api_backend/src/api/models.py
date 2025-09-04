from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class IDModel(BaseModel):
    """Common ID response model."""
    id: int = Field(..., description="Unique identifier")


# PUBLIC_INTERFACE
class AttendeeBase(BaseModel):
    """Base fields for attendee."""
    name: str = Field(..., description="Full name of the attendee", min_length=1, max_length=200)
    email: EmailStr = Field(..., description="Email of the attendee")


# PUBLIC_INTERFACE
class AttendeeCreate(AttendeeBase):
    """Payload to create an attendee."""
    pass


# PUBLIC_INTERFACE
class AttendeeUpdate(BaseModel):
    """Payload to update an attendee."""
    name: Optional[str] = Field(None, description="Full name of the attendee", min_length=1, max_length=200)
    email: Optional[EmailStr] = Field(None, description="Email of the attendee")


# PUBLIC_INTERFACE
class Attendee(AttendeeBase, IDModel):
    """Attendee response model."""
    events: List[int] = Field(default_factory=list, description="List of event IDs this attendee is associated with")


# PUBLIC_INTERFACE
class EventBase(BaseModel):
    """Base fields for event."""
    title: str = Field(..., description="Title of the event", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Description of the event", max_length=5000)
    location: Optional[str] = Field(None, description="Location of the event", max_length=1000)
    start_time: Optional[datetime] = Field(None, description="Start date-time of the event (ISO 8601)")
    end_time: Optional[datetime] = Field(None, description="End date-time of the event (ISO 8601)")


# PUBLIC_INTERFACE
class EventCreate(EventBase):
    """Payload to create an event."""
    pass


# PUBLIC_INTERFACE
class EventUpdate(BaseModel):
    """Payload to update an event."""
    title: Optional[str] = Field(None, description="Title of the event", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Description of the event", max_length=5000)
    location: Optional[str] = Field(None, description="Location of the event", max_length=1000)
    start_time: Optional[datetime] = Field(None, description="Start date-time of the event (ISO 8601)")
    end_time: Optional[datetime] = Field(None, description="End date-time of the event (ISO 8601)")


# PUBLIC_INTERFACE
class Event(EventBase, IDModel):
    """Event response model."""
    attendees: List[int] = Field(default_factory=list, description="List of attendee IDs associated to this event")
