"""
Debug script to visualize wall normals.
Generates SVG showing walls with their normal vectors.
"""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.primitives import Point, WallPolygon
from generators.visibility import Vector2D, build_polygon_vertices

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "samples" / "wall_data.json"
OUTPUT_FILE = PROJECT_ROOT / "output" / "walls_normals_debug.svg"


def load_walls() -> list[WallPolygon]:
    with open(DATA_FILE) as f:
        data = json.load(f)
    walls = []
    for wall_coords in data["walls"]:
        points = [Point(x=p[0], y=p[1]) for p in wall_coords]
        walls.append(WallPolygon(points=points))
    return walls


def normalize_coords(walls, width=800, height=600, padding=50):
    """Normalize to fit viewport."""
    all_x = [p.x for w in walls for p in w.points]
    all_y = [p.y for w in walls for p in w.points]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    scale = min((width - 2*padding) / (max_x - min_x),
                (height - 2*padding) / (max_y - min_y))
    
    def transform(x, y):
        return (padding + (x - min_x) * scale,
                padding + (y - min_y) * scale)
    
    return transform, scale


def main():
    walls = load_walls()
    transform, scale = normalize_coords(walls)
    
    svg_parts = ['<?xml version="1.0"?>\n<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">']
    svg_parts.append('<rect width="100%" height="100%" fill="#f5f5f5"/>')
    
    # Draw walls
    for i, wall in enumerate(walls):
        points_str = " ".join(f"{transform(p.x, p.y)[0]:.1f},{transform(p.x, p.y)[1]:.1f}" 
                              for p in wall.points)
        svg_parts.append(f'<polygon points="{points_str}" fill="#ddd" stroke="#000" stroke-width="1"/>')
    
    # Build polygon vertices using the correct algorithm
    vertices = build_polygon_vertices(walls)
    n = len(vertices)
    
    # Draw edges and normals using polygon-based approach
    for i in range(n):
        v_start = vertices[i]
        v_end = vertices[(i + 1) % n]
        
        # Transform edge endpoints
        sx, sy = transform(v_start.x, v_start.y)
        ex, ey = transform(v_end.x, v_end.y)
        
        # Draw edge (centerline)
        svg_parts.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                       f'stroke="green" stroke-width="2"/>')
        
        # Calculate normal using polygon approach (90° CW from edge direction)
        edge_dir = Vector2D(v_end.x - v_start.x, v_end.y - v_start.y)
        normal = edge_dir.perpendicular_cw().normalize()
        
        # Midpoint of edge
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        
        # Scale normal for visibility (30 pixels)
        arrow_len = 30
        nx, ny = mx + normal.x * arrow_len, my + normal.y * arrow_len
        
        svg_parts.append(f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" '
                       f'stroke="red" stroke-width="2" marker-end="url(#arrow)"/>')
        
        # Wall number
        svg_parts.append(f'<text x="{mx:.1f}" y="{my - 10:.1f}" text-anchor="middle" '
                       f'font-size="10" fill="blue">{i}</text>')
    
    # Arrow marker
    svg_parts.insert(1, '''<defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <path d="M0,0 L0,6 L9,3 z" fill="red"/>
        </marker>
    </defs>''')
    
    svg_parts.append('</svg>')
    
    OUTPUT_FILE.write_text('\n'.join(svg_parts))
    print(f"Generated: {OUTPUT_FILE}")
    print("Red arrows = normal vectors (should point OUTWARD from building)")


if __name__ == "__main__":
    main()
