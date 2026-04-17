from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base


class SackbotMessage(Base):
    __tablename__ = "sackbot_messages"

    id = Column(Integer, primary_key=True, index=True)
    trigger = Column(String(50), nullable=False, index=True)  # welcome, contextual, encouragement
    context = Column(String(100), nullable=True)              # e.g. page slug: "ideas", "projects"
    message = Column(Text, nullable=False)
    priority = Column(String(10), default="medium")           # low, medium, high
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
