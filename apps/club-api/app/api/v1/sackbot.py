from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response
from app.schemas.sackbot import SackbotMessageCreate
from app.services.sackbot_service import sackbot_service

router = APIRouter(prefix="/sackbot", tags=["sackbot"])


@router.get("/message")
def get_message(
    trigger: str | None = Query(None, description="welcome | contextual | encouragement"),
    context: str | None = Query(None, description="Page context, e.g. 'ideas', 'projects'"),
    db: Session = Depends(get_db),
):
    """Returns one Sackbot message, picking the best match for the given trigger/context."""
    msg = sackbot_service.get_message(db, trigger=trigger, context=context)
    return success_response(msg)


@router.get("/messages")
def list_messages(db: Session = Depends(get_db)):
    """List all messages (for admin use)."""
    return success_response(sackbot_service.get_all(db))


@router.post("/messages", status_code=201)
def create_message(data: SackbotMessageCreate, db: Session = Depends(get_db)):
    msg = sackbot_service.create(db, data)
    return success_response(msg)


@router.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    sackbot_service.delete(db, message_id)
