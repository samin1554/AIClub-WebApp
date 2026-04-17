from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response, paginated_response
from app.schemas.member import MemberCreate, MemberUpdate
from app.services.member_service import member_service

router = APIRouter(prefix="/members", tags=["members"])


@router.get("")
def list_members(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: str | None = None,
    skill: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    items, total = member_service.get_all(
        db, page=page, limit=limit, role=role, skill=skill, search=search
    )
    return paginated_response(items, total, page, limit)


@router.post("", status_code=201)
def create_member(data: MemberCreate, db: Session = Depends(get_db)):
    member = member_service.create(db, data)
    return success_response(member)


@router.get("/{member_id}")
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = member_service.get_by_id(db, member_id)
    return success_response(member)


@router.patch("/{member_id}")
def update_member(member_id: int, data: MemberUpdate, db: Session = Depends(get_db)):
    member = member_service.update(db, member_id, data)
    return success_response(member)
