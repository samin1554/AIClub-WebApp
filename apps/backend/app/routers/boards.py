from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Board, Stroke
from app.whiteboard_schemas import BoardCreate, BoardResponse, BoardListResponse, BoardUpdate

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    db_board = Board(
        title=board.title or "Untitled",
        owner_id=board.owner_id,
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


@router.get("", response_model=List[BoardListResponse])
def list_boards(db: Session = Depends(get_db)):
    boards = db.query(Board).order_by(Board.created_at.desc()).all()
    result = []
    for board in boards:
        result.append(BoardListResponse(
            id=board.id,
            title=board.title,
            owner_id=board.owner_id,
            created_at=board.created_at,
            stroke_count=len(board.strokes) if board.strokes else 0
        ))
    return result


@router.get("/{board_id}", response_model=BoardResponse)
def get_board(board_id: str, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return board


@router.patch("/{board_id}", response_model=BoardResponse)
def update_board(board_id: str, board_update: BoardUpdate, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board_update.title is not None:
        board.title = board_update.title
    db.commit()
    db.refresh(board)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(board_id: str, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    db.delete(board)
    db.commit()
    return None
