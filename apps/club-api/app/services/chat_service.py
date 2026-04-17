import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.chat import ChatSession, ChatMessage
from app.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
CONTEXT_WINDOW = 10  # number of recent messages to include


class ChatService:
    def _get_or_create_session(self, db: Session, session_key: str) -> ChatSession:
        session = db.query(ChatSession).filter(ChatSession.session_key == session_key).first()
        if not session:
            session = ChatSession(session_key=session_key)
            db.add(session)
            db.commit()
            db.refresh(session)
        return session

    async def send_message(self, db: Session, session_key: str, user_message: str) -> str:
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=503, detail="Chatbot not configured (missing GROQ_API_KEY)")

        session = self._get_or_create_session(db, session_key)

        # Load recent message history
        history = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(CONTEXT_WINDOW)
            .all()
        )
        history = list(reversed(history))

        messages = [{"role": "system", "content": settings.CHAT_SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_message})

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": messages,
                    "max_tokens": settings.GROQ_MAX_TOKENS,
                },
            )

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Groq API error")

        reply = response.json()["choices"][0]["message"]["content"]

        # Persist both messages
        db.add(ChatMessage(session_id=session.id, role="user", content=user_message))
        db.add(ChatMessage(session_id=session.id, role="assistant", content=reply))
        db.commit()

        return reply

    def get_history(self, db: Session, session_key: str) -> list[dict]:
        session = db.query(ChatSession).filter(ChatSession.session_key == session_key).first()
        if not session:
            return []
        return [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at,
            }
            for m in sorted(session.messages, key=lambda m: m.created_at)
        ]

    def clear_session(self, db: Session, session_key: str) -> None:
        session = db.query(ChatSession).filter(ChatSession.session_key == session_key).first()
        if session:
            db.delete(session)
            db.commit()


chat_service = ChatService()
