from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.event import Event, EventRSVP
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def get_all(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        upcoming: bool | None = None,
        past: bool | None = None,
    ) -> tuple[list[dict], int]:
        query = db.query(Event)
        now = datetime.now(timezone.utc)

        if upcoming:
            query = query.filter(Event.starts_at >= now)
            query = query.order_by(Event.starts_at.asc())
        elif past:
            query = query.filter(Event.starts_at < now)
            query = query.order_by(Event.starts_at.desc())
        else:
            query = query.order_by(Event.starts_at.desc())

        total = query.count()
        events = query.offset((page - 1) * limit).limit(limit).all()
        return [self._to_dict(e) for e in events], total

    def get_by_id(self, db: Session, event_id: int) -> dict:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return self._to_dict(event)

    def create(self, db: Session, data: EventCreate) -> dict:
        if data.ends_at <= data.starts_at:
            raise HTTPException(status_code=400, detail="ends_at must be after starts_at")
        event = Event(**data.model_dump())
        db.add(event)
        db.commit()
        db.refresh(event)
        return self._to_dict(event)

    def update(self, db: Session, event_id: int, data: EventUpdate) -> dict:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        # Validate times after update
        if event.ends_at <= event.starts_at:
            raise HTTPException(status_code=400, detail="ends_at must be after starts_at")
        db.commit()
        db.refresh(event)
        return self._to_dict(event)

    def delete(self, db: Session, event_id: int) -> None:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        db.delete(event)
        db.commit()

    def rsvp(self, db: Session, event_id: int, user_id: int, status: str = "going") -> dict:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Check capacity for "going" status
        if status == "going" and event.max_attendees:
            going_count = (
                db.query(EventRSVP)
                .filter(EventRSVP.event_id == event_id, EventRSVP.status == "going")
                .count()
            )
            existing = (
                db.query(EventRSVP)
                .filter(EventRSVP.event_id == event_id, EventRSVP.user_id == user_id)
                .first()
            )
            # Only check capacity if this is a new RSVP or changing from non-going to going
            if going_count >= event.max_attendees and (not existing or existing.status != "going"):
                raise HTTPException(status_code=409, detail="Event is at full capacity")

        existing = (
            db.query(EventRSVP)
            .filter(EventRSVP.event_id == event_id, EventRSVP.user_id == user_id)
            .first()
        )
        if existing:
            existing.status = status
            existing.updated_at = datetime.now(timezone.utc)
        else:
            existing = EventRSVP(event_id=event_id, user_id=user_id, status=status)
            db.add(existing)

        db.commit()
        db.refresh(event)
        return self._to_dict(event)

    def cancel_rsvp(self, db: Session, event_id: int, user_id: int) -> None:
        rsvp = (
            db.query(EventRSVP)
            .filter(EventRSVP.event_id == event_id, EventRSVP.user_id == user_id)
            .first()
        )
        if not rsvp:
            raise HTTPException(status_code=404, detail="RSVP not found")
        db.delete(rsvp)
        db.commit()

    def get_attendees(self, db: Session, event_id: int) -> list[dict]:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return [
            {
                "id": r.id,
                "event_id": r.event_id,
                "user_id": r.user_id,
                "status": r.status,
                "created_at": r.created_at,
            }
            for r in event.rsvps
        ]

    def generate_ics(self, db: Session, event_id: int) -> str:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        def fmt(dt: datetime) -> str:
            return dt.strftime("%Y%m%dT%H%M%SZ")

        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Club//Events//EN",
            "BEGIN:VEVENT",
            f"DTSTART:{fmt(event.starts_at)}",
            f"DTEND:{fmt(event.ends_at)}",
            f"SUMMARY:{event.title}",
        ]
        if event.description:
            escaped = event.description.replace("\n", "\\n")
            lines.append(f"DESCRIPTION:{escaped}")
        if event.location:
            lines.append(f"LOCATION:{event.location}")
        if event.meeting_url:
            lines.append(f"URL:{event.meeting_url}")
        lines.extend(["END:VEVENT", "END:VCALENDAR"])
        return "\r\n".join(lines)

    def _to_dict(self, event: Event) -> dict:
        going_count = sum(1 for r in event.rsvps if r.status == "going")
        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "starts_at": event.starts_at,
            "ends_at": event.ends_at,
            "location": event.location,
            "meeting_url": event.meeting_url,
            "meeting_password": event.meeting_password,
            "max_attendees": event.max_attendees,
            "is_public": event.is_public,
            "created_by_member_id": event.created_by_member_id,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
            "rsvp_count": going_count,
        }


event_service = EventService()
