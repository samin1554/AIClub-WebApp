from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=True)
    display_name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    skills = Column(JSON, default=list)
    github_url = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    website_url = Column(String(500), nullable=True)
    role = Column(String(20), default="member")  # member, lead, admin, alumni
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    graduation_year = Column(Integer, nullable=True)
