from pydantic import BaseModel, field_validator, model_serializer, ConfigDict
from typing import Optional, List, Any, Union
from datetime import datetime

class ContributorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    member_id: int
    role: str
    order: int

class ProjectBase(BaseModel):
    title: str
    summary: str
    content_md: Optional[str] = None
    tags: List[str] = []
    cover_url: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: str = "draft"
    
    @field_validator('tags', mode='before')
    @classmethod
    def convert_tags(cls, v: Any) -> List[str]:
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return list(v)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content_md: Optional[str] = None
    tags: Optional[List[str]] = None
    cover_url: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    contributors: List[ContributorSchema] = []
    
    @model_serializer(mode='wrap')
    def serialize_datetime(self, handler):
        data = handler(self)
        if 'created_at' in data and isinstance(data['created_at'], datetime):
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and isinstance(data['updated_at'], datetime):
            data['updated_at'] = data['updated_at'].isoformat()
        return data

class PaginatedProjectsResponse(BaseModel):
    data: List[ProjectResponse]
    meta: dict
