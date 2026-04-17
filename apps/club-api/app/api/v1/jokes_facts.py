from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response, paginated_response
from app.schemas.joke_fact import JokeFactCreate
from app.services.joke_fact_service import joke_fact_service

router = APIRouter(prefix="/jokes-facts", tags=["jokes-facts"])


@router.get("/random")
def get_random(
    type: str | None = Query(None, description="Filter by 'joke' or 'fact'"),
    db: Session = Depends(get_db),
):
    item = joke_fact_service.get_random(db, type=type)
    return success_response(item)


@router.get("")
def list_all(
    type: str | None = Query(None, description="Filter by 'joke' or 'fact'"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = joke_fact_service.get_all(db, type=type, page=page, limit=limit)
    return paginated_response(items, total, page, limit)


@router.post("", status_code=201)
def create(data: JokeFactCreate, db: Session = Depends(get_db)):
    item = joke_fact_service.create(db, data)
    return success_response(item)


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, db: Session = Depends(get_db)):
    joke_fact_service.delete(db, item_id)
