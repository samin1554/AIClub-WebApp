import { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { Whiteboard } from './components/Whiteboard';
import { BoardSelector } from './components/BoardSelector';
import { boardApi } from './services/api';
import { MusicLab } from './features/music/pages/MusicLab';
import type { BoardListItem } from './types';

function App() {
  const [boards, setBoards] = useState<BoardListItem[]>([]);
  const [selectedBoardId, setSelectedBoardId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  const loadBoards = async () => {
    try {
      const boardList = await boardApi.list();
      setBoards(boardList);
    } catch (error) {
      console.error('Failed to load boards:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBoards();
  }, []);

  const handleCreateBoard = async () => {
    try {
      const newBoard = await boardApi.create({ title: `Board ${boards.length + 1}` });
      await loadBoards();
      setSelectedBoardId(newBoard.id);
    } catch (error) {
      console.error('Failed to create board:', error);
    }
  };

  const handleSelectBoard = (id: string) => {
    setSelectedBoardId(id || null);
  };

  const handleDeleteBoard = async (id: string) => {
    if (!confirm('Are you sure you want to delete this board?')) return;
    
    try {
      await boardApi.delete(id);
      if (selectedBoardId === id) {
        setSelectedBoardId(null);
      }
      await loadBoards();
    } catch (error) {
      console.error('Failed to delete board:', error);
    }
  };

  const isMusicPage = location.pathname === '/music';

  if (isMusicPage) {
    return <MusicLab />;
  }

  return (
    <div className="flex flex-col h-screen">
      <header className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-300">
        <div className="flex items-center gap-6">
          <h1 className="text-xl font-bold text-gray-800">AI Club</h1>
          <nav className="flex gap-2">
            <Link 
              to="/"
              className={`px-4 py-2 rounded-lg transition-colors ${!selectedBoardId ? 'bg-purple-100 text-purple-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Whiteboard
            </Link>
            <Link 
              to="/music"
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Music Lab
            </Link>
          </nav>
        </div>
        <BoardSelector
          boards={boards}
          selectedBoardId={selectedBoardId}
          onSelect={handleSelectBoard}
          onCreate={handleCreateBoard}
          onDelete={handleDeleteBoard}
          loading={loading}
        />
      </header>
      <main className="flex-1 overflow-hidden">
        <Whiteboard boardId={selectedBoardId} />
      </main>
    </div>
  );
}

export default App;
