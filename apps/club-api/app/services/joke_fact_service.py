import random
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.joke_fact import JokeFact
from app.schemas.joke_fact import JokeFactCreate

VALID_TYPES = {"joke", "fact"}


class JokeFactService:
    def get_all(
        self,
        db: Session,
        type: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        query = db.query(JokeFact).filter(JokeFact.is_active == True)  # noqa: E712
        if type:
            if type not in VALID_TYPES:
                raise HTTPException(status_code=400, detail=f"type must be 'joke' or 'fact'")
            query = query.filter(JokeFact.type == type)
        total = query.count()
        items = query.order_by(JokeFact.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        return [self._to_dict(i) for i in items], total

    def get_random(self, db: Session, type: str | None = None) -> dict:
        query = db.query(JokeFact).filter(JokeFact.is_active == True)  # noqa: E712
        if type:
            if type not in VALID_TYPES:
                raise HTTPException(status_code=400, detail=f"type must be 'joke' or 'fact'")
            query = query.filter(JokeFact.type == type)
        items = query.all()
        if not items:
            raise HTTPException(status_code=404, detail="No jokes or facts found")
        return self._to_dict(random.choice(items))

    def create(self, db: Session, data: JokeFactCreate) -> dict:
        item = JokeFact(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return self._to_dict(item)

    def delete(self, db: Session, item_id: int) -> None:
        item = db.query(JokeFact).filter(JokeFact.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(item)
        db.commit()

    def _to_dict(self, item: JokeFact) -> dict:
        return {
            "id": item.id,
            "content": item.content,
            "type": item.type,
            "is_active": item.is_active,
            "created_at": item.created_at,
        }


joke_fact_service = JokeFactService()
