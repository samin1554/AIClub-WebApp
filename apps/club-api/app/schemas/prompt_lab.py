from pydantic import BaseModel
from typing import Literal


class PromptLabRequest(BaseModel):
    topic: str
    style: Literal["formal", "casual", "creative", "technical"] = "casual"
    mood: Literal["serious", "funny", "inspiring", "neutral"] = "neutral"
    length: Literal["short", "medium", "detailed"] = "medium"


class PromptLabResponse(BaseModel):
    prompt: str
    topic: str
    style: str
    mood: str
    length: str
