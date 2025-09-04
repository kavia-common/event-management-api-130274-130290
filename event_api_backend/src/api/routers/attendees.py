from typing import List

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field

from ..models import Attendee, AttendeeCreate, AttendeeUpdate
from ..repository import store

router = APIRouter(prefix="/attendees", tags=["Attendees"])


class MessageResponse(BaseModel):
    message: str = Field(..., description="Informational message")


@router.get(
    "",
    summary="List attendees",
    response_model=List[Attendee],
    responses={200: {"description": "List of all attendees"}},
)
# PUBLIC_INTERFACE
def list_attendees() -> List[Attendee]:
    """Return all attendees."""
    return store.list_attendees()


@router.post(
    "",
    summary="Create attendee",
    response_model=Attendee,
    status_code=status.HTTP_201_CREATED,
)
# PUBLIC_INTERFACE
def create_attendee(payload: AttendeeCreate) -> Attendee:
    """
    Create a new attendee.
    """
    return store.create_attendee(payload)


@router.get(
    "/{attendee_id}",
    summary="Get attendee by ID",
    response_model=Attendee,
    responses={404: {"model": MessageResponse, "description": "Attendee not found"}},
)
# PUBLIC_INTERFACE
def get_attendee(attendee_id: int = Path(..., description="ID of the attendee")) -> Attendee:
    """Retrieve an attendee by ID."""
    attendee = store.get_attendee(attendee_id)
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return attendee


@router.patch(
    "/{attendee_id}",
    summary="Update attendee",
    response_model=Attendee,
    responses={404: {"model": MessageResponse, "description": "Attendee not found"}},
)
# PUBLIC_INTERFACE
def update_attendee(
    attendee_id: int = Path(..., description="ID of the attendee"),
    payload: AttendeeUpdate = ...,
) -> Attendee:
    """Update fields of an attendee."""
    updated = store.update_attendee(attendee_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return updated


@router.delete(
    "/{attendee_id}",
    summary="Delete attendee",
    response_model=MessageResponse,
    responses={404: {"model": MessageResponse, "description": "Attendee not found"}},
)
# PUBLIC_INTERFACE
def delete_attendee(attendee_id: int = Path(..., description="ID of the attendee")) -> MessageResponse:
    """Delete an attendee by ID."""
    ok = store.delete_attendee(attendee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return MessageResponse(message="Attendee deleted")
