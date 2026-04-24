import secrets
from fastapi import APIRouter, Query, Header, HTTPException
from typing import Optional

from app.services.spotify_service import spotify_service
from app.services.playlist_service import playlist_service
from app.schemas.music import (
    TokenResponse,
    SpotifyUser,
    PlaybackState,
    SearchResponse,
    PlaylistResponse,
    MoodCategoriesResponse,
    MoodCategory,
)

router = APIRouter(prefix="/music", tags=["music"])

STATE_COOKIE_NAME = "spotify_auth_state"


@router.get("/auth/login")
async def login():
    state = secrets.token_urlsafe(32)
    auth_url = spotify_service.get_auth_url(state)
    return {"auth_url": auth_url, "state": state}


@router.get("/auth/callback")
async def callback(code: str = Query(...), state: str = Query(...)):
    try:
        token_data = await spotify_service.exchange_code_for_token(code)
        return {
            "access_token": token_data["access_token"],
            "token_type": token_data["token_type"],
            "expires_in": token_data["expires_in"],
            "refresh_token": token_data["refresh_token"],
            "scope": token_data["scope"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Auth failed: {str(e)}")


@router.get("/me")
async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        user = await spotify_service.get_current_user(access_token)
        return {
            "id": user.get("id"),
            "display_name": user.get("display_name"),
            "email": user.get("email"),
            "images": user.get("images", []),
            "product": user.get("product"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get user: {str(e)}")


@router.get("/me/player")
async def get_player(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        playback_state = await spotify_service.get_playback_state(access_token)
        return playback_state
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get player: {str(e)}")


@router.post("/me/player/play")
async def start_playback(
    device_id: Optional[str] = Query(None),
    context_uri: Optional[str] = Query(None),
    uris: Optional[str] = Query(None),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        uri_list = uris.split(",") if uris else None
        result = await spotify_service.start_playback(
            access_token, device_id, context_uri, uri_list
        )
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Playback failed: {str(e)}")


@router.post("/me/player/pause")
async def pause_playback(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        result = await spotify_service.pause_playback(access_token)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Pause failed: {str(e)}")


@router.post("/me/player/resume")
async def resume_playback(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        result = await spotify_service.resume_playback(access_token)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume failed: {str(e)}")


@router.post("/me/player/next")
async def skip_next(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        result = await spotify_service.skip_to_next(access_token)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Skip failed: {str(e)}")


@router.post("/me/player/previous")
async def skip_previous(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        result = await spotify_service.skip_to_previous(access_token)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Skip failed: {str(e)}")


@router.get("/search")
async def search(
    query: str = Query(...),
    limit: int = Query(20),
    offset: int = Query(0),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        results = await spotify_service.search(access_token, query, limit, offset)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")


@router.get("/playlist")
async def get_playlist(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        playlist = await spotify_service.get_playlist(
            access_token, playlist_service.playlist_id
        )
        return playlist
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get playlist: {str(e)}")


@router.get("/moods")
async def get_moods():
    return {"moods": playlist_service.get_all_moods()}


@router.get("/mood/{mood_id}")
async def get_mood_tracks(
    mood_id: str,
    limit: int = Query(20),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        query = playlist_service.get_mood_query(mood_id)
        results = await spotify_service.search(access_token, query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get mood tracks: {str(e)}")


@router.get("/devices")
async def get_devices(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    try:
        devices = await spotify_service.get_user_devices(access_token)
        return {"devices": devices}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get devices: {str(e)}")