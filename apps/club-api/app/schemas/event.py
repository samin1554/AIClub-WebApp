from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime
    location: str | None = None
    meeting_url: str | None = None
    meeting_password: str | None = None
    max_attendees: int | None = None
    is_public: bool = True
    created_by_member_id: int | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    location: str | None = None
    meeting_url: str | None = None
    meeting_password: str | None = None
    max_attendees: int | None = None
    is_public: bool | None = None


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime
    location: str | None = None
    meeting_url: str | None = None
    meeting_password: str | None = None
    max_attendees: int | None = None
    is_public: bool
    created_by_member_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
    rsvp_count: int = 0


class RSVPCreate(BaseModel):
    user_id: int
    status: str = "going"


class RSVPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: int
    status: str
    created_at: datetime
