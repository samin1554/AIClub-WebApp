import axios from 'axios';
import type { Board, BoardListItem, BoardCreate, Stroke, StrokeCreate } from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
});

export const boardApi = {
  list: async (): Promise<BoardListItem[]> => {
    const response = await api.get<BoardListItem[]>('/boards');
    return response.data;
  },

  get: async (id: string): Promise<Board> => {
    const response = await api.get<Board>(`/boards/${id}`);
    return response.data;
  },

  create: async (data: BoardCreate = {}): Promise<Board> => {
    const response = await api.post<Board>('/boards', data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/boards/${id}`);
  },
};

export const strokeApi = {
  list: async (boardId: string): Promise<Stroke[]> => {
    const response = await api.get<Stroke[]>(`/boards/${boardId}/strokes`);
    return response.data;
  },

  create: async (boardId: string, stroke: StrokeCreate): Promise<Stroke> => {
    const response = await api.post<Stroke>(`/boards/${boardId}/strokes`, stroke);
    return response.data;
  },

  delete: async (boardId: string, strokeId: string): Promise<void> => {
    await api.delete(`/boards/${boardId}/strokes/${strokeId}`);
  },

  clear: async (boardId: string): Promise<void> => {
    await api.delete(`/boards/${boardId}/strokes`);
  },
};
