export interface Point {
  x: number;
  y: number;
}

export interface Stroke {
  id: string;
  board_id: string;
  color: string;
  brush_size: number;
  points: Point[];
  created_at?: string;
}

export interface Board {
  id: string;
  title: string;
  owner_id: string | null;
  created_at: string;
  strokes?: Stroke[];
}

export interface BoardListItem {
  id: string;
  title: string;
  owner_id: string | null;
  created_at: string;
  stroke_count: number;
}

export interface StrokeCreate {
  color: string;
  brush_size: number;
  points: Point[];
}

export interface BoardCreate {
  title?: string;
  owner_id?: string;
}
