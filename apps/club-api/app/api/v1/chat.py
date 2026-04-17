from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=None)
async def send_message(data: ChatRequest, db: Session = Depends(get_db)):
    reply = await chat_service.send_message(db, data.session_key, data.message)
    return success_response({"session_key": data.session_key, "reply": reply})


@router.get("/{session_key}")
def get_history(session_key: str, db: Session = Depends(get_db)):
    messages = chat_service.get_history(db, session_key)
    return success_response(messages)


@router.delete("/{session_key}", status_code=204)
def clear_session(session_key: str, db: Session = Depends(get_db)):
    chat_service.clear_session(db, session_key)
