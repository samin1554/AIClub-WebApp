from fastapi import APIRouter

from app.response import success_response
from app.schemas.prompt_lab import PromptLabRequest
from app.services.prompt_lab_service import prompt_lab_service

router = APIRouter(prefix="/prompt-lab", tags=["prompt-lab"])


@router.post("/generate")
async def generate_prompt(data: PromptLabRequest):
    prompt = await prompt_lab_service.generate(data)
    return success_response({
        "prompt": prompt,
        "topic": data.topic,
        "style": data.style,
        "mood": data.mood,
        "length": data.length,
    })
