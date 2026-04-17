from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SERVICE_NAME: str = "club-api"
    SERVICE_PORT: int = 8020
    DATABASE_URL: str = "sqlite:///./club.db"
    CORS_ORIGINS: str = "http://localhost:3000"

    # Groq / Chatbot
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_MAX_TOKENS: int = 1024
    CHAT_SYSTEM_PROMPT: str = (
        "You are a helpful assistant for an AI Club. "
        "You help visitors learn about the club's projects, members, events, and ideas. "
        "Keep answers concise and friendly. "
        "If you don't know something specific about the club, say so and suggest they browse the site."
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
