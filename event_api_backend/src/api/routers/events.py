from typing import List

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field

from ..models import Event, EventCreate, EventUpdate, Attendee
from ..repository import store

router = APIRouter(prefix="/events", tags=["Events"])


class MessageResponse(BaseModel):
    message: str = Field(..., description="Informational message")


@router.get(
    "",
    summary="List events",
    response_model=List[Event],
    responses={200: {"description": "List of all events"}},
)
# PUBLIC_INTERFACE
def list_events() -> List[Event]:
    """Return all events."""
    return store.list_events()


@router.post(
    "",
    summary="Create event",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
)
# PUBLIC_INTERFACE
def create_event(payload: EventCreate) -> Event:
    """
    Create a new event.

    Parameters:
    - payload: EventCreate
    Returns:
    - Event
    """
    return store.create_event(payload)


@router.get(
    "/{event_id}",
    summary="Get event by ID",
    response_model=Event,
    responses={404: {"model": MessageResponse, "description": "Event not found"}},
)
# PUBLIC_INTERFACE
def get_event(
    event_id: int = Path(..., description="ID of the event"),
) -> Event:
    """Retrieve an event by ID."""
    event = store.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch(
    "/{event_id}",
    summary="Update event",
    response_model=Event,
    responses={404: {"model": MessageResponse, "description": "Event not found"}},
)
# PUBLIC_INTERFACE
def update_event(
    event_id: int = Path(..., description="ID of the event"),
    payload: EventUpdate = ...,
) -> Event:
    """Update fields of an event."""
    updated = store.update_event(event_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated


@router.delete(
    "/{event_id}",
    summary="Delete event",
    response_model=MessageResponse,
    responses={404: {"model": MessageResponse, "description": "Event not found"}},
)
# PUBLIC_INTERFACE
def delete_event(
    event_id: int = Path(..., description="ID of the event"),
) -> MessageResponse:
    """Delete an event by ID."""
    ok = store.delete_event(event_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return MessageResponse(message="Event deleted")


# Nested routes: /events/{event_id}/attendees

nested_router = APIRouter(prefix="/events/{event_id}/attendees", tags=["Event Attendees"])


@nested_router.get(
    "",
    summary="List attendees of event",
    response_model=List[Attendee],
    responses={404: {"model": MessageResponse, "description": "Event not found"}},
)
# PUBLIC_INTERFACE
def list_event_attendees(event_id: int = Path(..., description="ID of the event")) -> List[Attendee]:
    """
    List all attendees linked to a specific event.
    """
    attendees = store.list_event_attendees(event_id)
    if attendees is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return attendees


class LinkPayload(BaseModel):
    attendee_id: int = Field(..., description="Attendee ID to link/unlink")


@nested_router.post(
    "",
    summary="Add attendee to event",
    response_model=Event,
    responses={
        404: {"model": MessageResponse, "description": "Event or attendee not found"},
    },
)
# PUBLIC_INTERFACE
def add_attendee_to_event(
    payload: LinkPayload,
    event_id: int = Path(..., description="ID of the event"),
) -> Event:
    """
    Link an attendee to an event.
    """
    event, attendee = store.add_attendee_to_event(event_id, payload.attendee_id)
    if not event or not attendee:
        raise HTTPException(status_code=404, detail="Event or attendee not found")
    return event


@nested_router.delete(
    "",
    summary="Remove attendee from event",
    response_model=Event,
    responses={
        404: {"model": MessageResponse, "description": "Event or attendee not found"},
    },
)
# PUBLIC_INTERFACE
def remove_attendee_from_event(
    payload: LinkPayload,
    event_id: int = Path(..., description="ID of the event"),
) -> Event:
    """
    Unlink an attendee from an event.
    """
    event, attendee = store.remove_attendee_from_event(event_id, payload.attendee_id)
    if not event or not attendee:
        raise HTTPException(status_code=404, detail="Event or attendee not found")
    return event


# Register nested router onto main router path (so /events/... works)
router.include_router(nested_router)
