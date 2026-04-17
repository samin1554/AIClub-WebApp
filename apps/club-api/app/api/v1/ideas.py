from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response, paginated_response
from app.schemas.idea import IdeaCreate, IdeaUpdate, CommentCreate, VoteCreate
from app.services.idea_service import idea_service

router = APIRouter(prefix="/ideas", tags=["ideas"])


@router.get("")
def list_ideas(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    tag: str | None = None,
    search: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    items, total = idea_service.get_all(db, page=page, limit=limit, tag=tag, search=search, status=status)
    return paginated_response(items, total, page, limit)


@router.post("", status_code=201)
def create_idea(data: IdeaCreate, db: Session = Depends(get_db)):
    idea = idea_service.create(db, data)
    return success_response(idea)


@router.get("/{idea_id}")
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    idea = idea_service.get_by_id(db, idea_id)
    return success_response(idea)


@router.patch("/{idea_id}")
def update_idea(idea_id: int, data: IdeaUpdate, db: Session = Depends(get_db)):
    idea = idea_service.update(db, idea_id, data)
    return success_response(idea)


@router.delete("/{idea_id}", status_code=204)
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    idea_service.delete(db, idea_id)


@router.post("/{idea_id}/vote")
def vote_idea(idea_id: int, data: VoteCreate, db: Session = Depends(get_db)):
    idea = idea_service.vote(db, idea_id, data.member_id)
    return success_response(idea)


@router.delete("/{idea_id}/vote")
def unvote_idea(idea_id: int, member_id: int = Query(...), db: Session = Depends(get_db)):
    idea = idea_service.unvote(db, idea_id, member_id)
    return success_response(idea)


@router.get("/{idea_id}/comments")
def list_comments(idea_id: int, db: Session = Depends(get_db)):
    comments = idea_service.get_comments(db, idea_id)
    return success_response(comments)


@router.post("/{idea_id}/comments", status_code=201)
def add_comment(idea_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    comment = idea_service.add_comment(db, idea_id, data.member_id, data.body)
    return success_response(comment)


@router.delete("/{idea_id}/comments/{comment_id}", status_code=204)
def delete_comment(idea_id: int, comment_id: int, db: Session = Depends(get_db)):
    idea_service.delete_comment(db, comment_id)
