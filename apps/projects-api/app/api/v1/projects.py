from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, PaginatedProjectsResponse
)
from app.services.project_service import project_service

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("", response_model=PaginatedProjectsResponse)
def list_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    tag: Optional[str] = None,
    search: Optional[str] = None,
    status: str = "published",
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    projects, total = project_service.get_all(
        db, skip=skip, limit=limit, tag=tag, search=search, status=status
    )
    
    return {
        "data": projects,
        "meta": {
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit if total > 0 else 0
            }
        }
    }

@router.get("/{slug}", response_model=ProjectResponse)
def get_project(slug: str, db: Session = Depends(get_db)):
    project = project_service.get_by_slug(db, slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    return project_service.create(db, project, user_id=1)

@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
):
    updated = project_service.update(db, project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    success = project_service.delete(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

@router.get("/{project_id}/contributors")
def list_contributors(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = project_service.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.contributors

@router.post("/{project_id}/contributors")
def add_contributor(
    project_id: int,
    member_id: int,
    role: str,
    db: Session = Depends(get_db),
):
    project = project_service.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_service.add_contributor(db, project_id, member_id, role)

@router.delete("/{project_id}/contributors/{contributor_id}", status_code=204)
def remove_contributor(
    project_id: int,
    contributor_id: int,
    db: Session = Depends(get_db),
):
    success = project_service.remove_contributor(db, contributor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contributor not found")
