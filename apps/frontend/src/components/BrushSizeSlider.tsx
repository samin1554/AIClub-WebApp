interface BrushSizeSliderProps {
  size: number;
  onChange: (size: number) => void;
}

export function BrushSizeSlider({ size, onChange }: BrushSizeSliderProps) {
  return (
    <div className="flex items-center gap-2">
      <label className="text-sm text-gray-600">Size:</label>
      <input
        type="range"
        min="1"
        max="50"
        value={size}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-24 cursor-pointer"
      />
      <span className="text-sm text-gray-600 w-8">{size}px</span>
    </div>
  );
}
