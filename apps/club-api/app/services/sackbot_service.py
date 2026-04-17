import random
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sackbot import SackbotMessage
from app.schemas.sackbot import SackbotMessageCreate

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class SackbotService:
    def get_message(
        self,
        db: Session,
        trigger: str | None = None,
        context: str | None = None,
    ) -> dict:
        """
        Returns one message. Priority:
        1. Exact trigger + context match (high priority first)
        2. Trigger match with no context (fallback)
        3. Any enabled message (last resort)
        """
        query = db.query(SackbotMessage).filter(SackbotMessage.is_enabled == True)  # noqa: E712

        if trigger:
            query = query.filter(SackbotMessage.trigger == trigger)

        candidates = query.all()

        if not candidates:
            raise HTTPException(status_code=404, detail="No messages available")

        # Prefer context-specific matches, then sort by priority
        if context:
            exact = [m for m in candidates if m.context == context]
            if exact:
                candidates = exact

        # Among candidates, pick randomly from the highest-priority group
        top_priority = min(candidates, key=lambda m: PRIORITY_ORDER.get(m.priority, 1)).priority
        top_candidates = [m for m in candidates if m.priority == top_priority]

        return self._to_dict(random.choice(top_candidates))

    def get_all(self, db: Session) -> list[dict]:
        messages = db.query(SackbotMessage).order_by(
            SackbotMessage.trigger, SackbotMessage.priority
        ).all()
        return [self._to_dict(m) for m in messages]

    def create(self, db: Session, data: SackbotMessageCreate) -> dict:
        msg = SackbotMessage(**data.model_dump())
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return self._to_dict(msg)

    def delete(self, db: Session, message_id: int) -> None:
        msg = db.query(SackbotMessage).filter(SackbotMessage.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        db.delete(msg)
        db.commit()

    def _to_dict(self, msg: SackbotMessage) -> dict:
        return {
            "id": msg.id,
            "trigger": msg.trigger,
            "context": msg.context,
            "message": msg.message,
            "priority": msg.priority,
            "is_enabled": msg.is_enabled,
            "created_at": msg.created_at,
        }


sackbot_service = SackbotService()
