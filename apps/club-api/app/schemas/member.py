from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MemberCreate(BaseModel):
    display_name: str
    user_id: int | None = None
    bio: str | None = None
    avatar_url: str | None = None
    skills: list[str] = []
    github_url: str | None = None
    linkedin_url: str | None = None
    portfolio_url: str | None = None
    website_url: str | None = None
    role: str = "member"
    graduation_year: int | None = None


class MemberUpdate(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    skills: list[str] | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    portfolio_url: str | None = None
    website_url: str | None = None
    role: str | None = None
    graduation_year: int | None = None


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    display_name: str
    bio: str | None = None
    avatar_url: str | None = None
    skills: list[str] = []
    github_url: str | None = None
    linkedin_url: str | None = None
    portfolio_url: str | None = None
    website_url: str | None = None
    role: str
    joined_at: datetime
    graduation_year: int | None = None
