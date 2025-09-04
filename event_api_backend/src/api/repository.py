from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import (
    Event,
    EventCreate,
    EventUpdate,
    Attendee,
    AttendeeCreate,
    AttendeeUpdate,
)


class InMemoryStore:
    """
    Very simple in-memory storage for events and attendees with relationships.
    Not thread-safe; intended for demo and local development only.
    """

    def __init__(self) -> None:
        # Primary data stores
        self._events: Dict[int, Event] = {}
        self._attendees: Dict[int, Attendee] = {}

        # Auto-increment counters
        self._event_id = 0
        self._attendee_id = 0

    # PUBLIC_INTERFACE
    def list_events(self) -> List[Event]:
        """Return all events."""
        return list(self._events.values())

    # PUBLIC_INTERFACE
    def get_event(self, event_id: int) -> Optional[Event]:
        """Return event by id, if exists."""
        return self._events.get(event_id)

    # PUBLIC_INTERFACE
    def create_event(self, payload: EventCreate) -> Event:
        """Create and store a new event."""
        self._event_id += 1
        event = Event(id=self._event_id, attendees=[], **payload.model_dump())
        self._events[event.id] = event
        return event

    # PUBLIC_INTERFACE
    def update_event(self, event_id: int, payload: EventUpdate) -> Optional[Event]:
        """Update an existing event if present."""
        existing = self._events.get(event_id)
        if not existing:
            return None
        data = existing.model_dump()
        for k, v in payload.model_dump(exclude_unset=True).items():
            data[k] = v
        updated = Event(**data)
        self._events[event_id] = updated
        return updated

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: int) -> bool:
        """Delete an event and unlink it from related attendees."""
        event = self._events.pop(event_id, None)
        if not event:
            return False
        # Unlink from attendees
        for attendee_id in list(event.attendees):
            attendee = self._attendees.get(attendee_id)
            if attendee and event_id in attendee.events:
                updated_events = [e for e in attendee.events if e != event_id]
                self._attendees[attendee_id] = Attendee(
                    id=attendee.id,
                    name=attendee.name,
                    email=attendee.email,
                    events=updated_events,
                )
        return True

    # PUBLIC_INTERFACE
    def list_attendees(self) -> List[Attendee]:
        """Return all attendees."""
        return list(self._attendees.values())

    # PUBLIC_INTERFACE
    def get_attendee(self, attendee_id: int) -> Optional[Attendee]:
        """Return attendee by id, if exists."""
        return self._attendees.get(attendee_id)

    # PUBLIC_INTERFACE
    def create_attendee(self, payload: AttendeeCreate) -> Attendee:
        """Create and store a new attendee."""
        self._attendee_id += 1
        attendee = Attendee(id=self._attendee_id, events=[], **payload.model_dump())
        self._attendees[attendee.id] = attendee
        return attendee

    # PUBLIC_INTERFACE
    def update_attendee(self, attendee_id: int, payload: AttendeeUpdate) -> Optional[Attendee]:
        """Update an existing attendee if present."""
        existing = self._attendees.get(attendee_id)
        if not existing:
            return None
        data = existing.model_dump()
        for k, v in payload.model_dump(exclude_unset=True).items():
            data[k] = v
        updated = Attendee(**data)
        self._attendees[attendee_id] = updated
        return updated

    # PUBLIC_INTERFACE
    def delete_attendee(self, attendee_id: int) -> bool:
        """Delete an attendee and unlink them from related events."""
        attendee = self._attendees.pop(attendee_id, None)
        if not attendee:
            return False
        # Unlink from events
        for event_id in list(attendee.events):
            event = self._events.get(event_id)
            if event and attendee_id in event.attendees:
                updated_attendees = [a for a in event.attendees if a != attendee_id]
                self._events[event_id] = Event(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    location=event.location,
                    start_time=event.start_time,
                    end_time=event.end_time,
                    attendees=updated_attendees,
                )
        return True

    # Relationship management

    # PUBLIC_INTERFACE
    def add_attendee_to_event(self, event_id: int, attendee_id: int) -> Tuple[Optional[Event], Optional[Attendee]]:
        """
        Link an attendee to an event.
        Returns the updated (event, attendee) or (None, None) if either missing.
        """
        event = self._events.get(event_id)
        attendee = self._attendees.get(attendee_id)
        if not event or not attendee:
            return None, None

        if attendee_id not in event.attendees:
            event.attendees.append(attendee_id)
        if event_id not in attendee.events:
            attendee.events.append(event_id)

        # Re-assign to ensure new model instances (immutability preference)
        self._events[event_id] = Event(**event.model_dump())
        self._attendees[attendee_id] = Attendee(**attendee.model_dump())
        return self._events[event_id], self._attendees[attendee_id]

    # PUBLIC_INTERFACE
    def remove_attendee_from_event(self, event_id: int, attendee_id: int) -> Tuple[Optional[Event], Optional[Attendee]]:
        """
        Unlink an attendee from an event.
        Returns the updated (event, attendee) or (None, None) if either missing.
        """
        event = self._events.get(event_id)
        attendee = self._attendees.get(attendee_id)
        if not event or not attendee:
            return None, None

        if attendee_id in event.attendees:
            event.attendees = [a for a in event.attendees if a != attendee_id]
        if event_id in attendee.events:
            attendee.events = [e for e in attendee.events if e != event_id]

        self._events[event_id] = Event(**event.model_dump())
        self._attendees[attendee_id] = Attendee(**attendee.model_dump())
        return self._events[event_id], self._attendees[attendee_id]

    # PUBLIC_INTERFACE
    def list_event_attendees(self, event_id: int) -> Optional[List[Attendee]]:
        """List attendees for a specific event, or None if event not found."""
        event = self._events.get(event_id)
        if not event:
            return None
        return [self._attendees[a_id] for a_id in event.attendees if a_id in self._attendees]


# Singleton instance used by the routers
store = InMemoryStore()
