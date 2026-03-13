from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.v1 import projects

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=f"{settings.SERVICE_NAME}",
    description="Projects microservice for AI Club Web App",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "0.1.0"
    }
