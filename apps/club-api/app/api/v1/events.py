from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import success_response, paginated_response
from app.schemas.event import EventCreate, EventUpdate, RSVPCreate
from app.services.event_service import event_service

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    upcoming: bool | None = None,
    past: bool | None = None,
    db: Session = Depends(get_db),
):
    items, total = event_service.get_all(db, page=page, limit=limit, upcoming=upcoming, past=past)
    return paginated_response(items, total, page, limit)


@router.post("", status_code=201)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    event = event_service.create(db, data)
    return success_response(event)


@router.get("/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = event_service.get_by_id(db, event_id)
    return success_response(event)


@router.patch("/{event_id}")
def update_event(event_id: int, data: EventUpdate, db: Session = Depends(get_db)):
    event = event_service.update(db, event_id, data)
    return success_response(event)


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event_service.delete(db, event_id)


@router.post("/{event_id}/rsvp")
def rsvp_event(event_id: int, data: RSVPCreate, db: Session = Depends(get_db)):
    event = event_service.rsvp(db, event_id, data.user_id, data.status)
    return success_response(event)


@router.delete("/{event_id}/rsvp")
def cancel_rsvp(event_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    event_service.cancel_rsvp(db, event_id, user_id)
    return success_response({"message": "RSVP cancelled"})


@router.get("/{event_id}/attendees")
def list_attendees(event_id: int, db: Session = Depends(get_db)):
    attendees = event_service.get_attendees(db, event_id)
    return success_response(attendees)


@router.get("/{event_id}/calendar.ics")
def export_calendar(event_id: int, db: Session = Depends(get_db)):
    ics_content = event_service.generate_ics(db, event_id)
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=event-{event_id}.ics"},
    )
