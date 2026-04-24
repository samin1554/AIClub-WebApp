from pydantic import BaseModel
from typing import Optional, List


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class SpotifyUser(BaseModel):
    id: str
    display_name: str
    email: str
    images: List[dict] = []
    product: str


class Album(BaseModel):
    id: str
    name: str
    images: List[dict]


class Artist(BaseModel):
    id: str
    name: str


class Track(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    album: Album
    uri: str
    duration_ms: int
    preview_url: Optional[str] = None


class PlaybackState(BaseModel):
    device: dict
    repeat_state: str
    shuffle_state: bool
    context: Optional[dict] = None
    timestamp: int
    is_playing: bool
    item: Optional[dict] = None
    progress_ms: int


class SearchRequest(BaseModel):
    query: str
    limit: int = 20
    offset: int = 0


class SearchResponse(BaseModel):
    tracks: dict


class PlaylistResponse(BaseModel):
    id: str
    name: str
    description: str
    images: List[dict]
    tracks: dict


class MoodCategory(BaseModel):
    id: str
    name: str
    emoji: str
    query: str


class MoodCategoriesResponse(BaseModel):
    moods: List[MoodCategory]