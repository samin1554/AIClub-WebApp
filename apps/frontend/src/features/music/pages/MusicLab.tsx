import { useState, useEffect, useCallback } from 'react';
import { useSpotify, handleAuthCallback } from '../hooks/useSpotify';
import { usePlayer } from '../hooks/usePlayer';
import { spotifyApi } from '../api/spotifyApi';
import { LoginButton } from '../components/LoginButton';
import { NowPlaying } from '../components/NowPlaying';
import { PlaybackControls } from '../components/PlaybackControls';
import { Playlist } from '../components/Playlist';
import { SearchBar } from '../components/SearchBar';
import { SearchResults } from '../components/SearchResults';
import { MoodButtons } from '../components/MoodButtons';
import type { Track, MoodCategory, Playlist as PlaylistType } from '../types';

export function MusicLab() {
  const { isAuthenticated, isLoading: authLoading, isPremium, user, login } = useSpotify();
  const player = usePlayer(isPremium);
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Track[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [playlist, setPlaylist] = useState<PlaylistType | null>(null);
  const [isPlaylistLoading, setIsPlaylistLoading] = useState(false);
  const [moods, setMoods] = useState<MoodCategory[]>([]);
  const [selectedMood, setSelectedMood] = useState<string | null>(null);
  const [isMoodLoading, setIsMoodLoading] = useState(false);
  const [callbackHandled, setCallbackHandled] = useState(false);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    if (code && !callbackHandled) {
      setCallbackHandled(true);
      handleAuthCallback(code).then(() => {
        window.history.replaceState({}, '', '/music');
      }).catch((error) => {
        console.error('Auth callback failed:', error);
      });
    }
  }, [callbackHandled]);

  useEffect(() => {
    if (isAuthenticated) {
      setIsPlaylistLoading(true);
      spotifyApi.getPlaylist()
        .then(setPlaylist)
        .catch(console.error)
        .finally(() => setIsPlaylistLoading(false));
      
      spotifyApi.getMoods()
        .then((res) => setMoods(res.moods))
        .catch(console.error);
      
      player.initializePlayer();
    }
  }, [isAuthenticated, player]);

  const handleSearch = useCallback(async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    try {
      const results = await spotifyApi.search(searchQuery);
      setSearchResults(results.tracks.items);
      setSelectedMood(null);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  }, [searchQuery]);

  const handleMoodSelect = useCallback(async (moodId: string) => {
    setSelectedMood(moodId);
    setIsMoodLoading(true);
    setSearchQuery('');
    
    try {
      const results = await spotifyApi.getMoodTracks(moodId);
      setSearchResults(results.tracks.items);
    } catch (error) {
      console.error('Mood search failed:', error);
    } finally {
      setIsMoodLoading(false);
    }
  }, []);

  const handleTrackSelect = useCallback(async (uri: string) => {
    if (isPremium && player.isReady && player.deviceId) {
      await player.play(undefined, [uri]);
    } else {
      const spotifyUrl = uri.replace('spotify:', 'https://open.spotify.com/');
      window.open(spotifyUrl, '_blank');
    }
  }, [isPremium, player]);

  const handlePlayPause = useCallback(async () => {
    if (player.isPlaying) {
      await player.pause();
    } else {
      await player.resume();
    }
  }, [player]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 
                      flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-[#1DB954] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-white/60">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 
                      flex items-center justify-center p-8">
        <div className="max-w-md w-full text-center">
          <div className="mb-8">
            <h1 className="text-5xl font-bold text-white mb-4">AI Club</h1>
            <h2 className="text-2xl text-white/70">Music Lab</h2>
          </div>
          
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/10 mb-8">
            <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-[#1DB954] to-[#191414] 
                            rounded-full flex items-center justify-center">
              <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
              </svg>
            </div>
            
            <p className="text-white/60 mb-8">
              Connect your Spotify account to discover curated playlists, 
              search for songs, and control playback.
            </p>
            
            <LoginButton onLogin={login} />
          </div>
          
          <p className="text-white/40 text-sm">
            Powered by Spotify Web API
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-[#1DB954] to-[#191414] 
                            rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Music Lab</h1>
              <p className="text-white/50 text-sm">AI Club</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {user?.images?.[0] && (
              <img 
                src={user.images[0].url} 
                alt={user.display_name}
                className="w-10 h-10 rounded-full border-2 border-[#1DB954]"
              />
            )}
            <div className="text-right">
              <p className="text-white font-medium">{user?.display_name}</p>
              <p className="text-white/50 text-xs">{isPremium ? 'Premium' : 'Free'}</p>
            </div>
          </div>
        </header>

        {!isPremium && (
          <div className="mb-6 p-4 bg-yellow-500/20 border border-yellow-500/40 rounded-xl flex items-center gap-3">
            <svg className="w-6 h-6 text-yellow-400 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
              <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            <p className="text-yellow-200 text-sm">
              Spotify Premium is required for in-browser playback. 
              Non-premium users can use the "Open in Spotify" feature.
            </p>
          </div>
        )}

        <NowPlaying playbackState={player.currentTrack} isPremium={isPremium} />

        <PlaybackControls
          isPlaying={player.isPlaying}
          isPremium={isPremium}
          isReady={player.isReady}
          isLoading={!player.isReady && isPremium}
          onPlay={handlePlayPause}
          onPause={handlePlayPause}
          onNext={player.next}
          onPrevious={player.previous}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
          <div className="lg:col-span-2 space-y-6">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              onSearch={handleSearch}
              isLoading={isSearching}
            />

            <div>
              <h2 className="text-lg font-semibold text-white mb-4">Mood Categories</h2>
              <MoodButtons
                moods={moods}
                selectedMood={selectedMood}
                onMoodSelect={handleMoodSelect}
                isLoading={moods.length === 0}
              />
            </div>

            {(searchResults.length > 0 || isSearching || isMoodLoading) && (
              <div>
                <h2 className="text-lg font-semibold text-white mb-4">
                  {selectedMood ? `Mood: ${moods.find(m => m.id === selectedMood)?.name}` : 'Search Results'}
                </h2>
                <SearchResults
                  results={searchResults}
                  isLoading={isSearching || isMoodLoading}
                  onTrackSelect={handleTrackSelect}
                  searchQuery={searchQuery || selectedMood || ''}
                />
              </div>
            )}
          </div>

          <div>
            <Playlist
              playlist={playlist}
              isLoading={isPlaylistLoading}
              onTrackSelect={handleTrackSelect}
            />
          </div>
        </div>

        <footer className="mt-12 pt-8 border-t border-white/10 text-center">
          <p className="text-white/40 text-sm">
            AI Club Music Lab • Powered by Spotify
          </p>
        </footer>
      </div>
    </div>
  );
}