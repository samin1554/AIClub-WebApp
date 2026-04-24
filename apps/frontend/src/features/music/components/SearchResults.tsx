import type { Track } from '../types';

interface SearchResultsProps {
  results: Track[];
  isLoading: boolean;
  onTrackSelect: (track: Track) => void;
  searchQuery: string;
}

export function SearchResults({ results, isLoading, onTrackSelect, searchQuery }: SearchResultsProps) {
  if (!searchQuery && results.length === 0) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="animate-pulse bg-white/5 rounded-xl p-4">
            <div className="aspect-square bg-white/10 rounded-lg mb-3" />
            <div className="h-4 bg-white/10 rounded w-3/4 mb-2" />
            <div className="h-3 bg-white/10 rounded w-1/2" />
          </div>
        ))}
      </div>
    );
  }

  if (results.length === 0 && searchQuery) {
    return (
      <div className="text-center py-12">
        <svg className="w-16 h-16 mx-auto text-white/20 mb-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <p className="text-white/50">No results found for "{searchQuery}"</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {results.map((track) => (
        <button
          key={track.id}
          onClick={() => onTrackSelect(track)}
          className="group bg-white/5 hover:bg-white/10 rounded-xl p-4 transition-all 
                     text-left hover:scale-[1.02] active:scale-[0.98]"
        >
          <div className="relative aspect-square mb-3 overflow-hidden rounded-lg">
            <img
              src={track.album.images[0]?.url}
              alt={track.album.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 
                            transition-opacity flex items-center justify-center">
              <div className="w-12 h-12 rounded-full bg-[#1DB954] flex items-center justify-center 
                              shadow-lg transform scale-0 group-hover:scale-100 transition-transform">
                <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
          </div>
          <h3 className="text-white font-medium truncate mb-1 group-hover:text-[#1DB954] transition-colors">
            {track.name}
          </h3>
          <p className="text-white/50 text-sm truncate">
            {track.artists.map((a) => a.name).join(', ')}
          </p>
        </button>
      ))}
    </div>
  );
}