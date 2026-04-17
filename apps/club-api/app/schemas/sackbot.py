from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal


class SackbotMessageCreate(BaseModel):
    trigger: Literal["welcome", "contextual", "encouragement"]
    context: str | None = None
    message: str
    priority: Literal["low", "medium", "high"] = "medium"


class SackbotMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trigger: str
    context: str | None = None
    message: str
    priority: str
    is_enabled: bool
    created_at: datetime
