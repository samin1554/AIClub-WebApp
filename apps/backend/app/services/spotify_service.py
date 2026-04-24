import base64
import httpx
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

from app.config import settings


class SpotifyService:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI
        self.scopes = settings.SPOTIFY_SCOPES.split()
        self._token_cache: Optional[dict] = None

    def get_auth_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "state": state,
        }
        return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> dict:
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                },
                headers={"Authorization": f"Basic {auth_string}"},
            )
            response.raise_for_status()
            token_data = response.json()
            
            self._token_cache = {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": datetime.utcnow() + timedelta(seconds=token_data["expires_in"]),
            }
            return token_data

    async def refresh_token(self, refresh_token: str) -> dict:
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                headers={"Authorization": f"Basic {auth_string}"},
            )
            response.raise_for_status()
            token_data = response.json()
            
            self._token_cache = {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token", refresh_token),
                "expires_at": datetime.utcnow() + timedelta(seconds=token_data["expires_in"]),
            }
            return token_data

    async def get_current_user(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()

    async def get_playback_state(self, access_token: str) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/me/player",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code == 204:
                return None
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

    async def get_currently_playing(self, access_token: str) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/me/player/currently-playing",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code == 204:
                return None
            response.raise_for_status()
            return response.json()

    async def start_playback(self, access_token: str, device_id: str = None, context_uri: str = None, uris: list = None) -> bool:
        payload = {}
        if context_uri:
            payload["context_uri"] = context_uri
        if uris:
            payload["uris"] = uris
            
        async with httpx.AsyncClient() as client:
            url = "https://api.spotify.com/v1/me/player/play"
            if device_id:
                url += f"?device_id={device_id}"
            
            response = await client.put(
                url,
                json=payload if payload else None,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)

    async def pause_playback(self, access_token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                "https://api.spotify.com/v1/me/player/pause",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)

    async def resume_playback(self, access_token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                "https://api.spotify.com/v1/me/player/play",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)

    async def skip_to_next(self, access_token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.spotify.com/v1/me/player/next",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)

    async def skip_to_previous(self, access_token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.spotify.com/v1/me/player/previous",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)

    async def search(self, access_token: str, query: str, limit: int = 20, offset: int = 0) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/search",
                params={"q": query, "type": "track", "limit": limit, "offset": offset},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()

    async def get_playlist(self, access_token: str, playlist_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()

    async def get_user_devices(self, access_token: str) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/me/player/devices",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code == 204:
                return []
            response.raise_for_status()
            return response.json().get("devices", [])

    async def transfer_playback(self, access_token: str, device_id: str, force_play: bool = True) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                "https://api.spotify.com/v1/me/player",
                json={"device_ids": [device_id], "play": force_play},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            return response.status_code in (200, 204)


spotify_service = SpotifyService()