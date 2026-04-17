import httpx
from fastapi import HTTPException

from app.config import settings
from app.schemas.prompt_lab import PromptLabRequest

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

LENGTH_GUIDE = {
    "short": "1-2 sentences",
    "medium": "3-5 sentences",
    "detailed": "a full paragraph (6-10 sentences)",
}


class PromptLabService:
    async def generate(self, data: PromptLabRequest) -> str:
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=503, detail="Prompt Lab not configured (missing GROQ_API_KEY)")

        system = (
            "You are a creative prompt engineer. "
            "Generate a single, high-quality prompt based on the user's parameters. "
            "Output ONLY the prompt text itself — no preamble, no explanation, no quotes."
        )

        user_msg = (
            f"Generate a {data.mood}, {data.style} prompt about: {data.topic}. "
            f"The prompt should be {LENGTH_GUIDE[data.length]} long. "
            f"Make it specific, vivid, and immediately usable."
        )

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_msg},
                    ],
                    "max_tokens": 512,
                    "temperature": 0.9,
                },
            )

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Groq API error")

        return response.json()["choices"][0]["message"]["content"].strip()


prompt_lab_service = PromptLabService()
