import { useRef, useState, useCallback, useEffect } from 'react';
import type { Stroke, Point, StrokeCreate } from '../types';
import { strokeApi } from '../services/api';
import { useWebSocket } from './useWebSocket';

interface UseWhiteboardOptions {
  boardId: string | null;
  onStrokeSaved?: (stroke: Stroke) => void;
}

export function useWhiteboard({ boardId, onStrokeSaved }: UseWhiteboardOptions) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [currentColor, setCurrentColor] = useState('#000000');
  const [brushSize, setBrushSize] = useState(4);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentPoints, setCurrentPoints] = useState<Point[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  const { isConnected: wsConnected, send: sendWs } = useWebSocket({
    boardId,
    onMessage: (data: unknown) => {
      const msg = data as { type: string; data: Stroke };
      if (msg.type === 'stroke') {
        setStrokes((prev) => [...prev, msg.data]);
      } else if (msg.type === 'clear') {
        setStrokes([]);
      }
    },
  });

  useEffect(() => setIsConnected(wsConnected), [wsConnected]);

  const loadStrokes = useCallback(async () => {
    if (!boardId) return;
    try {
      const loadedStrokes = await strokeApi.list(boardId);
      setStrokes(loadedStrokes);
    } catch (error) {
      console.error('Failed to load strokes:', error);
    }
  }, [boardId]);

  useEffect(() => {
    loadStrokes();
  }, [loadStrokes]);

  const drawStroke = useCallback(
    (ctx: CanvasRenderingContext2D, stroke: Stroke) => {
      if (stroke.points.length < 2) return;

      ctx.beginPath();
      ctx.strokeStyle = stroke.color;
      ctx.lineWidth = stroke.brush_size;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      ctx.moveTo(stroke.points[0].x, stroke.points[0].y);
      for (let i = 1; i < stroke.points.length; i++) {
        ctx.lineTo(stroke.points[i].x, stroke.points[i].y);
      }
      ctx.stroke();
    },
    []
  );

  const redrawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Fill with white background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw all saved strokes
    for (const stroke of strokes) {
      drawStroke(ctx, stroke);
    }

    // Draw current stroke being drawn
    if (currentPoints.length > 1) {
      ctx.beginPath();
      ctx.strokeStyle = currentColor;
      ctx.lineWidth = brushSize;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.moveTo(currentPoints[0].x, currentPoints[0].y);
      for (let i = 1; i < currentPoints.length; i++) {
        ctx.lineTo(currentPoints[i].x, currentPoints[i].y);
      }
      ctx.stroke();
    }
  }, [strokes, currentPoints, currentColor, brushSize, drawStroke]);

  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas, boardId]);

  const getCanvasPoint = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>): Point => {
      const canvas = canvasRef.current;
      if (!canvas) return { x: 0, y: 0 };

      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      if ('touches' in e) {
        const touch = e.touches[0];
        return {
          x: (touch.clientX - rect.left) * scaleX,
          y: (touch.clientY - rect.top) * scaleY,
        };
      }

      return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY,
      };
    },
    []
  );

  const startDrawing = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
      const point = getCanvasPoint(e);
      setIsDrawing(true);
      setCurrentPoints([point]);
    },
    [getCanvasPoint]
  );

  const continueDrawing = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
      if (!isDrawing) return;
      const point = getCanvasPoint(e);
      setCurrentPoints((prev) => [...prev, point]);
    },
    [isDrawing, getCanvasPoint]
  );

  const finishDrawing = useCallback(async () => {
    if (!isDrawing || currentPoints.length < 2) {
      setIsDrawing(false);
      setCurrentPoints([]);
      return;
    }

    const newStroke: StrokeCreate = {
      color: currentColor,
      brush_size: brushSize,
      points: currentPoints,
    };

    if (boardId) {
      try {
        const savedStroke = await strokeApi.create(boardId, newStroke);
        setStrokes((prev) => [...prev, savedStroke]);
        onStrokeSaved?.(savedStroke);
        
        if (wsConnected) {
          sendWs({ type: 'stroke', data: savedStroke });
        }
      } catch (error) {
        console.error('Failed to save stroke:', error);
      }
    }

    setIsDrawing(false);
    setCurrentPoints([]);
  }, [isDrawing, currentPoints, currentColor, brushSize, boardId, onStrokeSaved, wsConnected, sendWs]);

  const undo = useCallback(async () => {
    if (strokes.length === 0 || !boardId) return;

    const lastStroke = strokes[strokes.length - 1];
    try {
      await strokeApi.delete(boardId, lastStroke.id);
      setStrokes((prev) => prev.slice(0, -1));
    } catch (error) {
      console.error('Failed to undo stroke:', error);
    }
  }, [strokes, boardId]);

  const clearBoard = useCallback(async () => {
    if (!boardId) return;

    try {
      await strokeApi.clear(boardId);
      setStrokes([]);
      if (wsConnected) {
        sendWs({ type: 'clear' });
      }
    } catch (error) {
      console.error('Failed to clear board:', error);
    }
  }, [boardId, wsConnected, sendWs]);

  const exportAsPng = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement('a');
    link.download = 'whiteboard.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  }, []);

  return {
    canvasRef,
    strokes,
    currentColor,
    setCurrentColor,
    brushSize,
    setBrushSize,
    isDrawing,
    isConnected,
    startDrawing,
    continueDrawing,
    finishDrawing,
    undo,
    clearBoard,
    exportAsPng,
    loadStrokes,
  };
}
