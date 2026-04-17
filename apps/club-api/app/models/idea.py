from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    pitch = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    status = Column(String(20), default="new")  # new, needs-work, accepted, rejected
    created_by_member_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    votes = relationship("IdeaVote", back_populates="idea", cascade="all, delete-orphan")
    comments = relationship("IdeaComment", back_populates="idea", cascade="all, delete-orphan")


class IdeaVote(Base):
    __tablename__ = "idea_votes"
    __table_args__ = (UniqueConstraint("idea_id", "member_id", name="uq_idea_vote"),)

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    idea = relationship("Idea", back_populates="votes")


class IdeaComment(Base):
    __tablename__ = "idea_comments"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    idea = relationship("Idea", back_populates="comments")
