from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response, paginated_response
from app.schemas.request import RequestCreate, RequestUpdate, RequestCommentCreate
from app.services.request_service import request_service

router = APIRouter(prefix="/requests", tags=["requests"])


@router.get("")
def list_requests(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
):
    items, total = request_service.get_all(db, page=page, limit=limit, status=status, priority=priority)
    return paginated_response(items, total, page, limit)


@router.post("", status_code=201)
def create_request(data: RequestCreate, db: Session = Depends(get_db)):
    req = request_service.create(db, data)
    return success_response(req)


@router.get("/{request_id}")
def get_request(request_id: int, db: Session = Depends(get_db)):
    req = request_service.get_by_id(db, request_id)
    return success_response(req)


@router.patch("/{request_id}")
def update_request(request_id: int, data: RequestUpdate, db: Session = Depends(get_db)):
    req = request_service.update(db, request_id, data)
    return success_response(req)


@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    request_service.delete(db, request_id)


@router.get("/{request_id}/comments")
def list_comments(request_id: int, db: Session = Depends(get_db)):
    comments = request_service.get_comments(db, request_id)
    return success_response(comments)


@router.post("/{request_id}/comments", status_code=201)
def add_comment(request_id: int, data: RequestCommentCreate, db: Session = Depends(get_db)):
    comment = request_service.add_comment(db, request_id, data.member_id, data.body)
    return success_response(comment)


@router.delete("/{request_id}/comments/{comment_id}", status_code=204)
def delete_comment(request_id: int, comment_id: int, db: Session = Depends(get_db)):
    request_service.delete_comment(db, comment_id)
