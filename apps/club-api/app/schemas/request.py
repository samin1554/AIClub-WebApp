from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RequestCreate(BaseModel):
    title: str
    problem: str
    desired_outcome: str
    constraints: str | None = None
    requester_name: str | None = None
    requester_contact: str | None = None


class RequestUpdate(BaseModel):
    title: str | None = None
    problem: str | None = None
    desired_outcome: str | None = None
    constraints: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_member_id: int | None = None


class RequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    problem: str
    desired_outcome: str
    constraints: str | None = None
    requester_name: str | None = None
    requester_contact: str | None = None
    status: str
    priority: str
    assigned_member_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
    comment_count: int = 0


class RequestCommentCreate(BaseModel):
    member_id: int
    body: str


class RequestCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    member_id: int
    body: str
    created_at: datetime
