import { useRef, useEffect, useCallback } from 'react';
import { useWhiteboard } from '../hooks/useWhiteboard';
import { Toolbar } from './Toolbar';

interface WhiteboardProps {
  boardId: string | null;
}

export function Whiteboard({ boardId }: WhiteboardProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  const {
    canvasRef,
    strokes,
    currentColor,
    setCurrentColor,
    brushSize,
    setBrushSize,
    startDrawing,
    continueDrawing,
    finishDrawing,
    undo,
    clearBoard,
    exportAsPng,
    loadStrokes,
  } = useWhiteboard({
    boardId,
  });

  const setupCanvasSize = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const rect = container.getBoundingClientRect();
    canvas.width = rect.width || 800;
    canvas.height = rect.height || 600;
  }, [canvasRef]);

  useEffect(() => {
    setupCanvasSize();
    window.addEventListener('resize', setupCanvasSize);
    return () => window.removeEventListener('resize', setupCanvasSize);
  }, [setupCanvasSize]);

  useEffect(() => {
    if (boardId) {
      loadStrokes();
    }
  }, [boardId, loadStrokes]);

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    startDrawing(e);
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    continueDrawing(e);
  };

  const handleMouseUp = () => {
    finishDrawing();
  };

  const handleTouchStart = (e: React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    startDrawing(e);
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    continueDrawing(e);
  };

  const handleTouchEnd = () => {
    finishDrawing();
  };

  return (
    <div className="flex h-full">
      <Toolbar
        color={currentColor}
        onColorChange={setCurrentColor}
        brushSize={brushSize}
        onBrushSizeChange={setBrushSize}
        onUndo={undo}
        onClear={clearBoard}
        onExport={exportAsPng}
        canUndo={strokes.length > 0}
      />
      <div ref={containerRef} className="flex-1 h-full bg-white">
        {boardId ? (
          <canvas
            ref={canvasRef}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            className="w-full h-full touch-none cursor-crosshair"
            width={800}
            height={600}
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <p>Select or create a board to start drawing</p>
          </div>
        )}
      </div>
    </div>
  );
}
