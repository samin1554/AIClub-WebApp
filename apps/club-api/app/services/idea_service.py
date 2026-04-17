from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.idea import Idea, IdeaVote, IdeaComment
from app.schemas.idea import IdeaCreate, IdeaUpdate


class IdeaService:
    def get_all(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        tag: str | None = None,
        search: str | None = None,
        status: str | None = None,
    ) -> tuple[list[dict], int]:
        query = db.query(Idea)

        if status:
            query = query.filter(Idea.status == status)
        if search:
            query = query.filter(
                Idea.title.ilike(f"%{search}%") | Idea.pitch.ilike(f"%{search}%")
            )

        total = query.count()
        ideas = query.order_by(Idea.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

        results = []
        for idea in ideas:
            idea_dict = self._to_dict(idea)
            if tag and tag not in (idea_dict.get("tags") or []):
                continue
            results.append(idea_dict)

        if tag:
            # Recount with tag filter applied
            all_ideas = query.all()
            total = sum(1 for i in all_ideas if tag in (i.tags or []))

        return results, total

    def get_by_id(self, db: Session, idea_id: int) -> dict:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        return self._to_dict(idea)

    def create(self, db: Session, data: IdeaCreate) -> dict:
        idea = Idea(**data.model_dump())
        db.add(idea)
        db.commit()
        db.refresh(idea)
        return self._to_dict(idea)

    def update(self, db: Session, idea_id: int, data: IdeaUpdate) -> dict:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(idea, key, value)
        db.commit()
        db.refresh(idea)
        return self._to_dict(idea)

    def delete(self, db: Session, idea_id: int) -> None:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        db.delete(idea)
        db.commit()

    def vote(self, db: Session, idea_id: int, member_id: int) -> dict:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        existing = (
            db.query(IdeaVote)
            .filter(IdeaVote.idea_id == idea_id, IdeaVote.member_id == member_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Already voted")

        vote = IdeaVote(idea_id=idea_id, member_id=member_id)
        db.add(vote)
        db.commit()
        db.refresh(idea)
        return self._to_dict(idea)

    def unvote(self, db: Session, idea_id: int, member_id: int) -> dict:
        vote = (
            db.query(IdeaVote)
            .filter(IdeaVote.idea_id == idea_id, IdeaVote.member_id == member_id)
            .first()
        )
        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        db.delete(vote)
        db.commit()

        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        return self._to_dict(idea)

    def get_comments(self, db: Session, idea_id: int) -> list[dict]:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        comments = (
            db.query(IdeaComment)
            .filter(IdeaComment.idea_id == idea_id)
            .order_by(IdeaComment.created_at.asc())
            .all()
        )
        return [
            {
                "id": c.id,
                "idea_id": c.idea_id,
                "member_id": c.member_id,
                "body": c.body,
                "created_at": c.created_at,
            }
            for c in comments
        ]

    def add_comment(self, db: Session, idea_id: int, member_id: int, body: str) -> dict:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        comment = IdeaComment(idea_id=idea_id, member_id=member_id, body=body)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return {
            "id": comment.id,
            "idea_id": comment.idea_id,
            "member_id": comment.member_id,
            "body": comment.body,
            "created_at": comment.created_at,
        }

    def delete_comment(self, db: Session, comment_id: int) -> None:
        comment = db.query(IdeaComment).filter(IdeaComment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        db.delete(comment)
        db.commit()

    def _to_dict(self, idea: Idea) -> dict:
        return {
            "id": idea.id,
            "title": idea.title,
            "pitch": idea.pitch,
            "description": idea.description,
            "tags": idea.tags or [],
            "status": idea.status,
            "created_by_member_id": idea.created_by_member_id,
            "created_at": idea.created_at,
            "updated_at": idea.updated_at,
            "vote_count": len(idea.votes),
            "comment_count": len(idea.comments),
        }


idea_service = IdeaService()
