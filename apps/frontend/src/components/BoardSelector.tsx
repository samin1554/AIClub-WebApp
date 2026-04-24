import type { BoardListItem } from '../types';

interface BoardSelectorProps {
  boards: BoardListItem[];
  selectedBoardId: string | null;
  onSelect: (id: string) => void;
  onCreate: () => void;
  onDelete: (id: string) => void;
  loading: boolean;
}

export function BoardSelector({
  boards,
  selectedBoardId,
  onSelect,
  onCreate,
  onDelete,
  loading,
}: BoardSelectorProps) {
  return (
    <div className="flex items-center gap-2">
      <select
        value={selectedBoardId || ''}
        onChange={(e) => onSelect(e.target.value)}
        disabled={loading}
        className="px-3 py-2 border border-gray-300 rounded bg-white text-gray-700"
      >
        <option value="">Select a board...</option>
        {boards.map((board) => (
          <option key={board.id} value={board.id}>
            {board.title} ({board.stroke_count} strokes)
          </option>
        ))}
      </select>

      <button
        onClick={onCreate}
        className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        New Board
      </button>

      {selectedBoardId && (
        <button
          onClick={() => onDelete(selectedBoardId)}
          className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
        >
          Delete
        </button>
      )}
    </div>
  );
}
