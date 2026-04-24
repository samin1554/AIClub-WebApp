import { useState, useCallback, useEffect, useRef } from 'react';
import { spotifyApi, auth } from '../api/spotifyApi';
import type { PlaybackState, Device } from '../types';

declare global {
  interface Window {
    Spotify: any;
  }
}

interface UsePlayerReturn {
  isReady: boolean;
  isPlaying: boolean;
  currentTrack: PlaybackState | null;
  devices: Device[];
  deviceId: string | null;
  isPremium: boolean;
  error: string | null;
  initializePlayer: () => Promise<void>;
  play: (contextUri?: string, uris?: string[]) => Promise<void>;
  pause: () => Promise<void>;
  resume: () => Promise<void>;
  next: () => Promise<void>;
  previous: () => Promise<void>;
  transferPlayback: (deviceId: string) => Promise<void>;
  refreshState: () => Promise<void>;
}

export function usePlayer(isPremiumUser: boolean): UsePlayerReturn {
  const [isReady, setIsReady] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrack, setCurrentTrack] = useState<PlaybackState | null>(null);
  const [devices, setDevices] = useState<Device[]>([]);
  const [deviceId, setDeviceId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const playerRef = useRef<any>(null);
  const tokenRef = useRef<string | null>(null);

  const loadScript = () => {
    return new Promise<void>((resolve, reject) => {
      if (window.Spotify) {
        resolve();
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://sdk.scdn.co/spotify-player.js';
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load Spotify SDK'));
      document.body.appendChild(script);
    });
  };

  const initializePlayer = useCallback(async () => {
    if (!isPremiumUser) {
      setError('Premium required for Web Playback SDK');
      return;
    }

    try {
      await loadScript();
      
      const token = auth.getAccessToken();
      if (!token) {
        setError('No access token');
        return;
      }
      tokenRef.current = token;

      window.onSpotifyWebPlaybackSDKReady = () => {
        const player = new window.Spotify.Player({
          name: 'AI Club Music Lab',
          getOAuthToken: (cb: (token: string) => void) => {
            cb(tokenRef.current || '');
          },
          volume: 0.5,
        });

        player.addListener('ready', ({ device_id }: { device_id: string }) => {
          setDeviceId(device_id);
          setIsReady(true);
          setError(null);
        });

        player.addListener('not_ready', ({ device_id }: { device_id: string }) => {
          setIsReady(false);
          console.log('Device offline:', device_id);
        });

        player.addListener('player_state_changed', (state: any) => {
          if (state) {
            setIsPlaying(!state.paused);
          }
        });

        player.addListener('initialization_error', ({ message }: { message: string }) => {
          setError(message);
        });

        player.addListener('authentication_error', ({ message }: { message: string }) => {
          setError('Authentication error: ' + message);
          auth.clearTokens();
        });

        player.addListener('account_error', ({ message }: { message: string }) => {
          setError('Premium account required: ' + message);
        });

        player.connect();
        playerRef.current = player;
      };

      const devicesData = await spotifyApi.getDevices();
      setDevices(devicesData.devices);
      
      const activeDevice = devicesData.devices.find((d: Device) => d.is_active);
      if (activeDevice) {
        setDeviceId(activeDevice.id);
      }

    } catch (err: any) {
      setError(err.message || 'Failed to initialize player');
    }
  }, [isPremiumUser]);

  const refreshState = useCallback(async () => {
    try {
      const state = await spotifyApi.getPlaybackState();
      setCurrentTrack(state);
      if (state) {
        setIsPlaying(state.is_playing);
      }
    } catch (err) {
      console.error('Failed to refresh playback state:', err);
    }
  }, []);

  const play = useCallback(async (contextUri?: string, uris?: string[]) => {
    if (deviceId) {
      await spotifyApi.startPlayback(deviceId, contextUri, uris);
      await refreshState();
    }
  }, [deviceId, refreshState]);

  const pause = useCallback(async () => {
    await spotifyApi.pausePlayback();
    setIsPlaying(false);
    await refreshState();
  }, [refreshState]);

  const resume = useCallback(async () => {
    await spotifyApi.resumePlayback();
    setIsPlaying(true);
    await refreshState();
  }, [refreshState]);

  const next = useCallback(async () => {
    await spotifyApi.skipNext();
    await refreshState();
  }, [refreshState]);

  const previous = useCallback(async () => {
    await spotifyApi.skipPrevious();
    await refreshState();
  }, [refreshState]);

  const transferPlayback = useCallback(async (newDeviceId: string) => {
    setDeviceId(newDeviceId);
  }, []);

  useEffect(() => {
    const interval = setInterval(refreshState, 5000);
    return () => clearInterval(interval);
  }, [refreshState]);

  useEffect(() => {
    if (isReady && playerRef.current) {
      refreshState();
    }
  }, [isReady, refreshState]);

  return {
    isReady,
    isPlaying,
    currentTrack,
    devices,
    deviceId,
    isPremium: isPremiumUser,
    error,
    initializePlayer,
    play,
    pause,
    resume,
    next,
    previous,
    transferPlayback,
    refreshState,
  };
}