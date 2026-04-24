import axios from 'axios';
import type { 
  TokenResponse, 
  SpotifyUser, 
  PlaybackState, 
  SearchResults, 
  Playlist,
  MoodCategory,
  Device 
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('spotify_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const spotifyApi = {
  async getAuthUrl(): Promise<{ auth_url: string; state: string }> {
    const response = await api.get('/music/auth/login');
    return response.data;
  },

  async handleCallback(code: string): Promise<TokenResponse> {
    const response = await api.get('/music/auth/callback', { params: { code } });
    return response.data;
  },

  async getCurrentUser(): Promise<SpotifyUser> {
    const response = await api.get('/music/me');
    return response.data;
  },

  async getPlaybackState(): Promise<PlaybackState | null> {
    const response = await api.get('/music/me/player');
    return response.data;
  },

  async startPlayback(deviceId?: string, contextUri?: string, uris?: string[]): Promise<{ success: boolean }> {
    const params: Record<string, string> = {};
    if (deviceId) params.device_id = deviceId;
    if (contextUri) params.context_uri = contextUri;
    if (uris) params.uris = uris.join(',');
    
    const response = await api.post('/music/me/player/play', null, { params });
    return response.data;
  },

  async pausePlayback(): Promise<{ success: boolean }> {
    const response = await api.post('/music/me/player/pause');
    return response.data;
  },

  async resumePlayback(): Promise<{ success: boolean }> {
    const response = await api.post('/music/me/player/resume');
    return response.data;
  },

  async skipNext(): Promise<{ success: boolean }> {
    const response = await api.post('/music/me/player/next');
    return response.data;
  },

  async skipPrevious(): Promise<{ success: boolean }> {
    const response = await api.post('/music/me/player/previous');
    return response.data;
  },

  async search(query: string, limit = 20, offset = 0): Promise<SearchResults> {
    const response = await api.get('/music/search', { params: { query, limit, offset } });
    return response.data;
  },

  async getPlaylist(): Promise<Playlist> {
    const response = await api.get('/music/playlist');
    return response.data;
  },

  async getMoods(): Promise<{ moods: MoodCategory[] }> {
    const response = await api.get('/music/moods');
    return response.data;
  },

  async getMoodTracks(moodId: string, limit = 20): Promise<SearchResults> {
    const response = await api.get(`/music/mood/${moodId}`, { params: { limit } });
    return response.data;
  },

  async getDevices(): Promise<{ devices: Device[] }> {
    const response = await api.get('/music/devices');
    return response.data;
  },
};

export const auth = {
  setTokens(tokenData: TokenResponse) {
    localStorage.setItem('spotify_access_token', tokenData.access_token);
    localStorage.setItem('spotify_refresh_token', tokenData.refresh_token);
    localStorage.setItem('spotify_token_expires_at', String(Date.now() + tokenData.expires_in * 1000));
  },

  getAccessToken(): string | null {
    return localStorage.getItem('spotify_access_token');
  },

  getRefreshToken(): string | null {
    return localStorage.getItem('spotify_refresh_token');
  },

  isTokenExpired(): boolean {
    const expiresAt = localStorage.getItem('spotify_token_expires_at');
    if (!expiresAt) return true;
    return Date.now() > parseInt(expiresAt);
  },

  clearTokens() {
    localStorage.removeItem('spotify_access_token');
    localStorage.removeItem('spotify_refresh_token');
    localStorage.removeItem('spotify_token_expires_at');
  },

  isAuthenticated(): boolean {
    return !!this.getAccessToken() && !this.isTokenExpired();
  },
};

export default api;