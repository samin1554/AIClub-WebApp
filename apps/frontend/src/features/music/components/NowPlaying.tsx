import type { PlaybackState } from '../types';

interface NowPlayingProps {
  playbackState: PlaybackState | null;
  isPremium: boolean;
}

export function NowPlaying({ playbackState, isPremium }: NowPlayingProps) {
  const track = playbackState?.item;
  
  if (!track) {
    return (
      <div className="bg-gradient-to-br from-purple-900/80 to-indigo-900/80 
                      backdrop-blur-lg rounded-2xl p-8 border border-white/10">
        <div className="flex flex-col items-center justify-center min-h-[300px] text-center">
          <div className="w-48 h-48 bg-white/10 rounded-2xl flex items-center justify-center mb-6">
            <svg className="w-24 h-24 text-white/30" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">No Track Playing</h2>
          <p className="text-white/60">Search for a song or select from the playlist</p>
          
          {!isPremium && (
            <div className="mt-6 px-4 py-2 bg-yellow-500/20 border border-yellow-500/40 rounded-lg">
              <p className="text-yellow-300 text-sm">
                ⚠️ Spotify Premium required for in-browser playback
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }

  const albumArt = track.album.images[0]?.url;
  const artistName = track.artists.map((a) => a.name).join(', ');
  const progressMs = playbackState?.progress_ms || 0;
  const durationMs = track.duration_ms;
  const progressPercent = (progressMs / durationMs) * 100;

  const formatTime = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-gradient-to-br from-purple-900/80 to-indigo-900/80 
                    backdrop-blur-lg rounded-2xl p-8 border border-white/10">
      <div className="flex flex-col md:flex-row gap-8 items-center">
        <div className="relative group">
          <img
            src={albumArt}
            alt={track.album.name}
            className="w-48 h-48 rounded-2xl shadow-2xl object-cover
                       group-hover:scale-105 transition-transform duration-300"
          />
          {playbackState?.is_playing && (
            <div className="absolute inset-0 bg-black/20 rounded-2xl animate-pulse" />
          )}
        </div>
        
        <div className="flex-1 text-center md:text-left">
          <h2 className="text-sm uppercase tracking-wider text-white/50 mb-2">Now Playing</h2>
          <h1 className="text-3xl font-bold text-white mb-2 truncate">{track.name}</h1>
          <p className="text-xl text-white/70 mb-4">{artistName}</p>
          
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5 text-white/50" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
              </svg>
              <span className="text-white/60 text-sm">{track.album.name}</span>
            </div>
            
            {playbackState?.device && (
              <div className="flex items-center gap-3">
                <svg className="w-5 h-5 text-white/50" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M4 6h18V4H4c-1.1 0-2 .9-2 2v11H0v3h14v-3H4V6zm19 2h-6c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h6c.55 0 1-.45 1-1V9c0-.55-.45-1-1-1zm-1 9h-4v-7h4v7z"/>
                </svg>
                <span className="text-white/60 text-sm">
                  {playbackState.device.name} ({playbackState.device.type})
                </span>
              </div>
            )}
          </div>
          
          <div className="mt-6">
            <div className="relative h-1 bg-white/20 rounded-full overflow-hidden">
              <div 
                className="absolute left-0 top-0 h-full bg-[#1DB954] rounded-full transition-all duration-1000"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
            <div className="flex justify-between mt-2 text-sm text-white/50">
              <span>{formatTime(progressMs)}</span>
              <span>{formatTime(durationMs)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}