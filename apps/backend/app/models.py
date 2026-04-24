import uuid
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, default="Untitled")
    owner_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    strokes = relationship("Stroke", back_populates="board", cascade="all, delete-orphan")


class Stroke(Base):
    __tablename__ = "strokes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    board_id = Column(String(36), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    color = Column(String(7), nullable=False)
    brush_size = Column(Integer, nullable=False)
    _points = Column("points", Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    board = relationship("Board", back_populates="strokes")

    @property
    def points(self):
        if self._points is None:
            return []
        if isinstance(self._points, list):
            return self._points
        try:
            return json.loads(str(self._points))
        except:
            return []

    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self._points = json.dumps(value)
        else:
            self._points = value
