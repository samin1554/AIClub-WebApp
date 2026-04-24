export interface SpotifyUser {
  id: string;
  display_name: string;
  email: string;
  images: { url: string }[];
  product: string;
}

export interface SpotifyImage {
  url: string;
  height?: number;
  width?: number;
}

export interface Album {
  id: string;
  name: string;
  images: SpotifyImage[];
}

export interface Artist {
  id: string;
  name: string;
}

export interface Track {
  id: string;
  name: string;
  artists: Artist[];
  album: Album;
  uri: string;
  duration_ms: number;
  preview_url?: string;
}

export interface PlaybackState {
  device: {
    id: string;
    name: string;
    type: string;
    is_active: boolean;
  };
  repeat_state: 'off' | 'track' | 'context';
  shuffle_state: boolean;
  context?: {
    uri: string;
    type: string;
  };
  timestamp: number;
  is_playing: boolean;
  item?: Track;
  progress_ms: number;
}

export interface SearchResults {
  tracks: {
    items: Track[];
    total: number;
    limit: number;
    offset: number;
  };
}

export interface Playlist {
  id: string;
  name: string;
  description: string;
  images: SpotifyImage[];
  tracks: {
    items: {
      track: Track;
    }[];
    total: number;
  };
}

export interface MoodCategory {
  id: string;
  name: string;
  emoji: string;
  query: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string;
  scope: string;
}

export interface Device {
  id: string;
  name: string;
  type: string;
  is_active: boolean;
}