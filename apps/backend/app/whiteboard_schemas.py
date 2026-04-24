from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float


class StrokeBase(BaseModel):
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    brush_size: int = Field(..., ge=1, le=100)
    points: List[Point]


class StrokeCreate(StrokeBase):
    pass


class StrokeResponse(StrokeBase):
    id: str
    board_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class BoardBase(BaseModel):
    title: str = "Untitled"
    owner_id: Optional[str] = None


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: Optional[str] = None


class BoardResponse(BoardBase):
    id: str
    created_at: datetime
    strokes: List[StrokeResponse] = []

    class Config:
        from_attributes = True


class BoardListResponse(BaseModel):
    id: str
    title: str
    owner_id: Optional[str]
    created_at: datetime
    stroke_count: int = 0

    class Config:
        from_attributes = True
