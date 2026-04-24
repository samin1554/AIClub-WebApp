import { useState, useCallback, useEffect } from 'react';
import { spotifyApi, auth } from '../api/spotifyApi';
import type { SpotifyUser, TokenResponse } from '../types';

interface UseSpotifyReturn {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: SpotifyUser | null;
  isPremium: boolean;
  login: () => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export function useSpotify(): UseSpotifyReturn {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<SpotifyUser | null>(null);
  const [isPremium, setIsPremium] = useState(false);

  const checkAuth = useCallback(async () => {
    if (auth.isAuthenticated()) {
      setIsAuthenticated(true);
      try {
        const userData = await spotifyApi.getCurrentUser();
        setUser(userData);
        setIsPremium(userData.product === 'premium');
      } catch {
        auth.clearTokens();
        setIsAuthenticated(false);
      }
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = useCallback(async () => {
    try {
      const { auth_url } = await spotifyApi.getAuthUrl();
      window.location.href = auth_url;
    } catch (error) {
      console.error('Login failed:', error);
    }
  }, []);

  const logout = useCallback(() => {
    auth.clearTokens();
    setIsAuthenticated(false);
    setUser(null);
    setIsPremium(false);
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const userData = await spotifyApi.getCurrentUser();
      setUser(userData);
      setIsPremium(userData.product === 'premium');
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  }, []);

  return {
    isAuthenticated,
    isLoading,
    user,
    isPremium,
    login,
    logout,
    refreshUser,
  };
}

export function handleAuthCallback(code: string): Promise<TokenResponse> {
return spotifyApi.handleCallback(code).then((tokenData) => {
  auth.setTokens(tokenData);
  return tokenData;
  });
}