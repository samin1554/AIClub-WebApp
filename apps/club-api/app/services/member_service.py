from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


class MemberService:
    def get_all(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        role: str | None = None,
        skill: str | None = None,
        search: str | None = None,
    ) -> tuple[list[dict], int]:
        query = db.query(Member)

        if role:
            query = query.filter(Member.role == role)
        if search:
            query = query.filter(Member.display_name.ilike(f"%{search}%"))

        all_members = query.order_by(Member.joined_at.desc()).all()

        # Filter by skill in-memory (JSON column)
        if skill:
            skill_lower = skill.lower()
            all_members = [
                m for m in all_members if skill_lower in [s.lower() for s in (m.skills or [])]
            ]

        total = len(all_members)
        start = (page - 1) * limit
        members = all_members[start : start + limit]
        return [self._to_dict(m) for m in members], total

    def get_by_id(self, db: Session, member_id: int) -> dict:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return self._to_dict(member)

    def create(self, db: Session, data: MemberCreate) -> dict:
        member = Member(**data.model_dump())
        db.add(member)
        db.commit()
        db.refresh(member)
        return self._to_dict(member)

    def update(self, db: Session, member_id: int, data: MemberUpdate) -> dict:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
        return self._to_dict(member)

    def _to_dict(self, member: Member) -> dict:
        return {
            "id": member.id,
            "user_id": member.user_id,
            "display_name": member.display_name,
            "bio": member.bio,
            "avatar_url": member.avatar_url,
            "skills": member.skills or [],
            "github_url": member.github_url,
            "linkedin_url": member.linkedin_url,
            "portfolio_url": member.portfolio_url,
            "website_url": member.website_url,
            "role": member.role,
            "joined_at": member.joined_at,
            "graduation_year": member.graduation_year,
        }


member_service = MemberService()
