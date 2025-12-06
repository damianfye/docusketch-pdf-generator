"""
Visualize wall_data.json to understand the polygon layout.

Generates an SVG with:
- Each wall polygon numbered (0-18)
- Color gradient from red (first) to blue (last) to see order
- Outputs to output/walls_debug.svg

Run: python scripts/visualize_walls.py
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "samples" / "wall_data.json"
OUTPUT_FILE = PROJECT_ROOT / "output" / "walls_debug.svg"


def load_walls() -> list[list[list[float]]]:
    """Load wall polygons from JSON."""
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data["walls"]


def get_gradient_color(index: int, total: int) -> str:
    """Generate color from red (0) to blue (total-1)."""
    if total <= 1:
        return "#FF0000"
    
    # Interpolate from red to blue via green
    t = index / (total - 1)
    
    if t < 0.5:
        # Red to Green
        r = int(255 * (1 - 2 * t))
        g = int(255 * 2 * t)
        b = 0
    else:
        # Green to Blue
        r = 0
        g = int(255 * (2 - 2 * t))
        b = int(255 * (2 * t - 1))
    
    return f"#{r:02x}{g:02x}{b:02x}"


def normalize_walls(walls: list[list[list[float]]], width: float, height: float, padding: float = 20):
    """Normalize wall coordinates to fit in viewport."""
    # Find bounding box
    all_x = [p[0] for wall in walls for p in wall]
    all_y = [p[1] for wall in walls for p in wall]
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    data_width = max_x - min_x
    data_height = max_y - min_y
    
    # Scale to fit
    available_width = width - 2 * padding
    available_height = height - 2 * padding
    scale = min(available_width / data_width, available_height / data_height)
    
    # Transform walls
    normalized = []
    for wall in walls:
        new_wall = []
        for p in wall:
            new_x = padding + (p[0] - min_x) * scale
            new_y = padding + (p[1] - min_y) * scale
            new_wall.append([new_x, new_y])
        normalized.append(new_wall)
    
    return normalized


def get_polygon_center(points: list[list[float]]) -> tuple[float, float]:
    """Get center of polygon for label placement."""
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    return cx, cy


def generate_svg(walls: list[list[list[float]]], width: float = 800, height: float = 600) -> str:
    """Generate debug SVG."""
    normalized = normalize_walls(walls, width, height)
    total = len(normalized)
    
    polygons = []
    labels = []
    
    for i, wall in enumerate(normalized):
        color = get_gradient_color(i, total)
        points_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in wall)
        
        # Polygon
        polygons.append(f'''<polygon 
            points="{points_str}" 
            fill="{color}" 
            fill-opacity="0.7"
            stroke="#000" 
            stroke-width="1"
        />''')
        
        # Label
        cx, cy = get_polygon_center(wall)
        labels.append(f'''<text 
            x="{cx:.1f}" 
            y="{cy:.1f}" 
            text-anchor="middle" 
            dominant-baseline="middle"
            font-size="12"
            font-weight="bold"
            fill="#000"
        >{i}</text>''')
    
    # Legend
    legend_y = height - 30
    legend = f'''
        <text x="10" y="{legend_y}" font-size="12" fill="#FF0000">0 = First (Red)</text>
        <text x="200" y="{legend_y}" font-size="12" fill="#0000FF">{total-1} = Last (Blue)</text>
        <text x="400" y="{legend_y}" font-size="12" fill="#666">Total: {total} walls</text>
    '''
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#f5f5f5"/>
    
    <!-- Walls -->
    {"".join(polygons)}
    
    <!-- Labels -->
    {"".join(labels)}
    
    <!-- Legend -->
    {legend}
</svg>'''


def main():
    print(f"Loading walls from: {DATA_FILE}")
    walls = load_walls()
    print(f"Found {len(walls)} wall polygons")
    
    svg = generate_svg(walls)
    
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(svg)
    print(f"Generated: {OUTPUT_FILE}")
    print("\nOpen the SVG in a browser to see the visualization!")


if __name__ == "__main__":
    main()
