from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.v1 import ideas, events, members, requests, chat, jokes_facts, prompt_lab, sackbot

# Import all models so they register with Base.metadata
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.SERVICE_NAME,
    description="AI Club API — Ideas, Events, Members, Requests, Chat, Jokes/Facts, Prompt Lab",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ideas.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(members.router, prefix="/api/v1")
app.include_router(requests.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(jokes_facts.router, prefix="/api/v1")
app.include_router(prompt_lab.router, prefix="/api/v1")
app.include_router(sackbot.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "0.1.0",
    }
