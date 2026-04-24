import { ColorPicker } from './ColorPicker';
import { BrushSizeSlider } from './BrushSizeSlider';

interface ToolbarProps {
  color: string;
  onColorChange: (color: string) => void;
  brushSize: number;
  onBrushSizeChange: (size: number) => void;
  onUndo: () => void;
  onClear: () => void;
  onExport: () => void;
  canUndo: boolean;
}

export function Toolbar({
  color,
  onColorChange,
  brushSize,
  onBrushSizeChange,
  onUndo,
  onClear,
  onExport,
  canUndo,
}: ToolbarProps) {
  return (
    <div className="flex flex-col gap-4 p-4 bg-gray-100 border-r border-gray-300 w-48 h-full">
      <h2 className="text-lg font-semibold text-gray-700">Toolbar</h2>
      
      <ColorPicker color={color} onChange={onColorChange} />
      
      <BrushSizeSlider size={brushSize} onChange={onBrushSizeChange} />
      
      <div className="flex flex-col gap-2 mt-4">
        <button
          onClick={onUndo}
          disabled={!canUndo}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Undo
        </button>
        
        <button
          onClick={onClear}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
        >
          Clear
        </button>
        
        <button
          onClick={onExport}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
        >
          Export PNG
        </button>
      </div>
    </div>
  );
}
