from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    problem = Column(Text, nullable=False)
    desired_outcome = Column(Text, nullable=False)
    constraints = Column(Text, nullable=True)
    requester_name = Column(String(100), nullable=True)
    requester_contact = Column(String(200), nullable=True)
    status = Column(String(20), default="new")  # new, reviewing, accepted, in_progress, shipped, rejected
    priority = Column(String(10), default="medium")  # low, medium, high
    assigned_member_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    comments = relationship("RequestComment", back_populates="request", cascade="all, delete-orphan")


class RequestComment(Base):
    __tablename__ = "request_comments"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    request = relationship("Request", back_populates="comments")
