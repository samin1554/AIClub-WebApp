interface PlaybackControlsProps {
  isPlaying: boolean;
  isPremium: boolean;
  isReady: boolean;
  isLoading: boolean;
  onPlay: () => void;
  onPause: () => void;
  onNext: () => void;
  onPrevious: () => void;
}

export function PlaybackControls({
  isPlaying,
  isPremium,
  isReady,
  isLoading,
  onPlay,
  onPause,
  onNext,
  onPrevious,
}: PlaybackControlsProps) {
  const isDisabled = !isPremium || !isReady;

  return (
    <div className="flex items-center justify-center gap-4 py-6">
      <button
        onClick={onPrevious}
        disabled={isDisabled || isLoading}
        className="p-3 rounded-full bg-white/10 text-white hover:bg-white/20 
                   disabled:opacity-30 disabled:cursor-not-allowed transition-all
                   hover:scale-110 active:scale-95"
        title="Previous"
      >
        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
        </svg>
      </button>

      <button
        onClick={isPlaying ? onPause : onPlay}
        disabled={isDisabled || isLoading}
        className="p-5 rounded-full bg-[#1DB954] text-white 
                   hover:bg-[#1ed760] disabled:bg-white/30 disabled:cursor-not-allowed 
                   transition-all hover:scale-110 active:scale-95 shadow-lg"
        title={isPlaying ? 'Pause' : 'Play'}
      >
        {isLoading ? (
          <svg className="w-8 h-8 animate-spin" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : isPlaying ? (
          <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
        ) : (
          <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        )}
      </button>

      <button
        onClick={onNext}
        disabled={isDisabled || isLoading}
        className="p-3 rounded-full bg-white/10 text-white hover:bg-white/20 
                   disabled:opacity-30 disabled:cursor-not-allowed transition-all
                   hover:scale-110 active:scale-95"
        title="Next"
      >
        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
        </svg>
      </button>

      {!isPremium && (
        <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 
                        px-3 py-1 bg-yellow-500/90 text-white text-xs rounded-lg
                        opacity-0 group-hover:opacity-100 transition-opacity">
          Premium required for playback
        </div>
      )}
    </div>
  );
}