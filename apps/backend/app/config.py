from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite:///./whiteboard.db"

    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""
    SPOTIFY_REDIRECT_URI: str = "https://your-vercel-app.vercel.app/callback"
    SPOTIFY_SCOPES: str = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private streaming"
    AI_CLUB_PLAYLIST_ID: str = "placeholder_playlist_id"
    SECRET_KEY: str = "dev_secret_key_change_in_production"


settings = Settings()
