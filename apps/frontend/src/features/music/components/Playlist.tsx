import type { Playlist } from '../types';

interface PlaylistProps {
  playlist: Playlist | null;
  isLoading: boolean;
  onTrackSelect: (uri: string) => void;
}

export function Playlist({ playlist, isLoading, onTrackSelect }: PlaylistProps) {
  if (isLoading) {
    return (
      <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="w-12 h-12 bg-white/10 rounded-lg" />
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-white/10 rounded w-3/4" />
                <div className="h-3 bg-white/10 rounded w-1/2" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!playlist) {
    return (
      <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
        <h2 className="text-xl font-bold text-white mb-4">AI Club Playlist</h2>
        <p className="text-white/50 text-center py-8">
          Configure your playlist ID in the environment variables
        </p>
      </div>
    );
  }

  const tracks = playlist.tracks?.items?.map((item) => item.track).filter(Boolean) || [];

  return (
    <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
      <div className="flex items-center gap-4 mb-6">
        {playlist.images?.[0] && (
          <img
            src={playlist.images[0].url}
            alt={playlist.name}
            className="w-16 h-16 rounded-lg shadow-lg"
          />
        )}
        <div>
          <h2 className="text-xl font-bold text-white">{playlist.name}</h2>
          <p className="text-white/50 text-sm line-clamp-1">
            {playlist.description || 'AI Club curated playlist'}
          </p>
        </div>
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-white/20">
        {tracks.map((track: any, index: number) => (
          <button
            key={`${track.id}-${index}`}
            onClick={() => onTrackSelect(track.uri)}
            className="w-full flex items-center gap-4 p-3 rounded-xl 
                       hover:bg-white/10 transition-colors text-left group"
          >
            <span className="w-8 text-white/40 text-sm">{index + 1}</span>
            {track.album?.images?.[2] && (
              <img
                src={track.album.images[2].url}
                alt={track.album.name}
                className="w-10 h-10 rounded-md"
              />
            )}
            <div className="flex-1 min-w-0">
              <p className="text-white font-medium truncate group-hover:text-[#1DB954] transition-colors">
                {track.name}
              </p>
              <p className="text-white/50 text-sm truncate">
                {track.artists?.map((a: any) => a.name).join(', ')}
              </p>
            </div>
            <svg className="w-5 h-5 text-white/30 group-hover:text-[#1DB954] transition-colors" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>
        ))}
      </div>

      {playlist.tracks?.total > tracks.length && (
        <p className="text-white/40 text-sm text-center mt-4">
          + {playlist.tracks.total - tracks.length} more tracks
        </p>
      )}
    </div>
  );
}