from typing import List
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Board, Stroke
from app.whiteboard_schemas import StrokeCreate, StrokeResponse

router = APIRouter(prefix="/boards/{board_id}/strokes", tags=["strokes"])


@router.post("", response_model=StrokeResponse, status_code=status.HTTP_201_CREATED)
def create_stroke(board_id: str, stroke: StrokeCreate, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    db_stroke = Stroke(
        board_id=board_id,
        color=stroke.color,
        brush_size=stroke.brush_size,
        _points=json.dumps([point.model_dump() for point in stroke.points])
    )
    db.add(db_stroke)
    db.commit()
    db.refresh(db_stroke)
    return db_stroke


@router.get("", response_model=List[StrokeResponse])
def list_strokes(board_id: str, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    strokes = db.query(Stroke).filter(Stroke.board_id == board_id).order_by(Stroke.created_at).all()
    return strokes


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_strokes(board_id: str, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    db.query(Stroke).filter(Stroke.board_id == board_id).delete()
    db.commit()
    return None


@router.delete("/{stroke_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stroke(board_id: str, stroke_id: str, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    stroke = db.query(Stroke).filter(Stroke.id == stroke_id, Stroke.board_id == board_id).first()
    if not stroke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stroke not found")
    
    db.delete(stroke)
    db.commit()
    return None
