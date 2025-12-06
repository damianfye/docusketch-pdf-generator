"""
Test the visibility algorithm with real wall data.

Run: python scripts/test_visibility.py
"""

import json
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.primitives import Point, WallPolygon
from generators.visibility import (
    ViewDirection,
    get_visible_wall_indices,
    extract_centerline,
)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "samples" / "wall_data.json"


def load_walls() -> list[WallPolygon]:
    """Load wall polygons from JSON."""
    with open(DATA_FILE) as f:
        data = json.load(f)
    
    walls = []
    for wall_coords in data["walls"]:
        points = [Point(x=p[0], y=p[1]) for p in wall_coords]
        walls.append(WallPolygon(points=points))
    
    return walls


def main():
    print(f"Loading walls from: {DATA_FILE}")
    walls = load_walls()
    print(f"Loaded {len(walls)} walls\n")
    
    # Test each direction
    for direction in ViewDirection:
        visible = get_visible_wall_indices(walls, direction)
        print(f"{direction.value.upper():8} visible walls: {sorted(visible)}")
    
    print("\n--- Centerline extraction test ---")
    # Show first few centerlines
    for i in range(min(3, len(walls))):
        wall = walls[i]
        segment = extract_centerline(wall)
        print(f"Wall {i}: centerline from ({segment.start.x:.0f}, {segment.start.y:.0f}) "
              f"to ({segment.end.x:.0f}, {segment.end.y:.0f})")


if __name__ == "__main__":
    main()
