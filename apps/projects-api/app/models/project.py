from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    content_md = Column(Text, nullable=True)
    tags = Column(ARRAY(String), default=[])
    cover_url = Column(String, nullable=True)
    repo_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    contributors = relationship("ProjectContributor", back_populates="project")

class ProjectContributor(Base):
    __tablename__ = "project_contributors"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    member_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    order = Column(Integer, default=0)
    
    project = relationship("Project", back_populates="contributors")
