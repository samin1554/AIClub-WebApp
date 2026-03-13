from sqlalchemy.orm import Session
from app.models.project import Project, ProjectContributor
from app.schemas.project import ProjectCreate, ProjectUpdate
from slugify import slugify
from typing import Optional, List, Tuple

class ProjectService:
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        status: str = "published"
    ) -> Tuple[List[Project], int]:
        query = db.query(Project)
        
        if status:
            query = query.filter(Project.status == status)
        
        if tag:
            query = query.filter(Project.tags.contains([tag]))
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Project.title.ilike(search_term) |
                Project.summary.ilike(search_term)
            )
        
        total = query.count()
        projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
        
        return projects, total
    
    def get_by_slug(self, db: Session, slug: str) -> Optional[Project]:
        return db.query(Project).filter(Project.slug == slug).first()
    
    def get_by_id(self, db: Session, project_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()
    
    def create(self, db: Session, data: ProjectCreate, user_id: int) -> Project:
        base_slug = slugify(data.title)
        slug = base_slug
        counter = 1
        
        while db.query(Project).filter(Project.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        project = Project(
            slug=slug,
            title=data.title,
            summary=data.summary,
            content_md=data.content_md,
            tags=data.tags,
            cover_url=data.cover_url,
            repo_url=data.repo_url,
            demo_url=data.demo_url,
            status=data.status,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    def update(self, db: Session, project_id: int, data: ProjectUpdate) -> Optional[Project]:
        project = self.get_by_id(db, project_id)
        if not project:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        return project
    
    def delete(self, db: Session, project_id: int) -> bool:
        project = self.get_by_id(db, project_id)
        if not project:
            return False
        
        db.delete(project)
        db.commit()
        return True
    
    def add_contributor(
        self, db: Session, project_id: int, member_id: int, role: str
    ) -> ProjectContributor:
        contributor = ProjectContributor(
            project_id=project_id,
            member_id=member_id,
            role=role
        )
        db.add(contributor)
        db.commit()
        db.refresh(contributor)
        return contributor
    
    def remove_contributor(self, db: Session, contributor_id: int) -> bool:
        contributor = db.query(ProjectContributor).filter(
            ProjectContributor.id == contributor_id
        ).first()
        
        if not contributor:
            return False
        
        db.delete(contributor)
        db.commit()
        return True

project_service = ProjectService()
