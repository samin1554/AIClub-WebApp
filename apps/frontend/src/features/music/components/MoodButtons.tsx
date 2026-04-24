import type { MoodCategory } from '../types';

interface MoodButtonsProps {
  moods: MoodCategory[];
  selectedMood: string | null;
  onMoodSelect: (moodId: string) => void;
  isLoading?: boolean;
}

const moodGradients: Record<string, string> = {
  study: 'from-blue-500/20 to-purple-500/20 hover:from-blue-500/30 hover:to-purple-500/30',
  hackathon: 'from-orange-500/20 to-red-500/20 hover:from-orange-500/30 hover:to-red-500/30',
  chill: 'from-green-500/20 to-teal-500/20 hover:from-green-500/30 hover:to-teal-500/30',
  latenight: 'from-indigo-500/20 to-purple-500/20 hover:from-indigo-500/30 hover:to-purple-500/30',
  demo: 'from-yellow-500/20 to-orange-500/20 hover:from-yellow-500/30 hover:to-orange-500/30',
};

const moodBorders: Record<string, string> = {
  study: 'border-blue-500/30',
  hackathon: 'border-orange-500/30',
  chill: 'border-green-500/30',
  latenight: 'border-indigo-500/30',
  demo: 'border-yellow-500/30',
};

export function MoodButtons({ moods, selectedMood, onMoodSelect, isLoading }: MoodButtonsProps) {
  if (isLoading) {
    return (
      <div className="flex gap-3 overflow-x-auto pb-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex-shrink-0 px-5 py-3 bg-white/5 rounded-xl border border-white/10 animate-pulse">
            <div className="w-8 h-8 bg-white/10 rounded-full mb-2" />
            <div className="h-4 bg-white/10 rounded w-24" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-white/20">
      {moods.map((mood) => {
        const isSelected = selectedMood === mood.id;
        const gradient = moodGradients[mood.id] || 'from-white/10 to-white/5';
        const borderColor = moodBorders[mood.id] || 'border-white/20';
        
        return (
          <button
            key={mood.id}
            onClick={() => onMoodSelect(mood.id)}
            className={`flex-shrink-0 px-5 py-3 rounded-xl border transition-all duration-200
                       ${isSelected 
                         ? `bg-gradient-to-r ${gradient} ${borderColor} scale-105` 
                         : 'bg-white/5 border-white/10 hover:bg-white/10'
                       }`}
          >
            <span className="text-2xl mb-2 block">{mood.emoji}</span>
            <span className={`text-sm font-medium ${isSelected ? 'text-white' : 'text-white/70'}`}>
              {mood.name}
            </span>
          </button>
        );
      })}
    </div>
  );
}