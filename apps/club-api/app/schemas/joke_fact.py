from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal


class JokeFactCreate(BaseModel):
    content: str
    type: Literal["joke", "fact"]


class JokeFactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    type: str
    is_active: bool
    created_at: datetime
