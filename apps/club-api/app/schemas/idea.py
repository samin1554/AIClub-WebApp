from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IdeaCreate(BaseModel):
    title: str
    pitch: str
    description: str | None = None
    tags: list[str] = []
    created_by_member_id: int | None = None


class IdeaUpdate(BaseModel):
    title: str | None = None
    pitch: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class IdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    pitch: str
    description: str | None = None
    tags: list[str] = []
    status: str
    created_by_member_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
    vote_count: int = 0
    comment_count: int = 0


class CommentCreate(BaseModel):
    member_id: int
    body: str


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    idea_id: int
    member_id: int
    body: str
    created_at: datetime


class VoteCreate(BaseModel):
    member_id: int
