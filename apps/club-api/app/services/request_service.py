from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.request import Request, RequestComment
from app.schemas.request import RequestCreate, RequestUpdate

VALID_STATUSES = {"new", "reviewing", "accepted", "in_progress", "shipped", "rejected"}
VALID_PRIORITIES = {"low", "medium", "high"}


class RequestService:
    def get_all(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        status: str | None = None,
        priority: str | None = None,
    ) -> tuple[list[dict], int]:
        query = db.query(Request)
        if status:
            query = query.filter(Request.status == status)
        if priority:
            query = query.filter(Request.priority == priority)

        total = query.count()
        requests = query.order_by(Request.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        return [self._to_dict(r) for r in requests], total

    def get_by_id(self, db: Session, request_id: int) -> dict:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        return self._to_dict(req)

    def create(self, db: Session, data: RequestCreate) -> dict:
        req = Request(**data.model_dump())
        db.add(req)
        db.commit()
        db.refresh(req)
        return self._to_dict(req)

    def update(self, db: Session, request_id: int, data: RequestUpdate) -> dict:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")

        update_data = data.model_dump(exclude_unset=True)
        if "status" in update_data and update_data["status"] not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {VALID_STATUSES}")
        if "priority" in update_data and update_data["priority"] not in VALID_PRIORITIES:
            raise HTTPException(status_code=400, detail=f"Invalid priority. Must be one of: {VALID_PRIORITIES}")

        for key, value in update_data.items():
            setattr(req, key, value)
        db.commit()
        db.refresh(req)
        return self._to_dict(req)

    def delete(self, db: Session, request_id: int) -> None:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        db.delete(req)
        db.commit()

    def get_comments(self, db: Session, request_id: int) -> list[dict]:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        return [
            {
                "id": c.id,
                "request_id": c.request_id,
                "member_id": c.member_id,
                "body": c.body,
                "created_at": c.created_at,
            }
            for c in sorted(req.comments, key=lambda c: c.created_at)
        ]

    def add_comment(self, db: Session, request_id: int, member_id: int, body: str) -> dict:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        comment = RequestComment(request_id=request_id, member_id=member_id, body=body)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return {
            "id": comment.id,
            "request_id": comment.request_id,
            "member_id": comment.member_id,
            "body": comment.body,
            "created_at": comment.created_at,
        }

    def delete_comment(self, db: Session, comment_id: int) -> None:
        comment = db.query(RequestComment).filter(RequestComment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        db.delete(comment)
        db.commit()

    def _to_dict(self, req: Request) -> dict:
        return {
            "id": req.id,
            "title": req.title,
            "problem": req.problem,
            "desired_outcome": req.desired_outcome,
            "constraints": req.constraints,
            "requester_name": req.requester_name,
            "requester_contact": req.requester_contact,
            "status": req.status,
            "priority": req.priority,
            "assigned_member_id": req.assigned_member_id,
            "created_at": req.created_at,
            "updated_at": req.updated_at,
            "comment_count": len(req.comments),
        }


request_service = RequestService()
