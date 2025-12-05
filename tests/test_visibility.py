"""
Tests for the wall visibility algorithm.

Based on visual inspection of walls_normals_debug.svg with real wall_data.json.
"""

import json
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.primitives import Point, WallPolygon
from generators.visibility import (
    ViewDirection,
    Vector2D,
    Segment,
    extract_centerline,
    get_visible_wall_indices,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def real_walls() -> list[WallPolygon]:
    """Load real wall data from wall_data.json."""
    data_file = Path(__file__).parent.parent / "data" / "samples" / "wall_data.json"
    with open(data_file) as f:
        data = json.load(f)
    
    walls = []
    for wall_coords in data["walls"]:
        points = [Point(x=p[0], y=p[1]) for p in wall_coords]
        walls.append(WallPolygon(points=points))
    
    return walls


# =============================================================================
# EXPECTED NORMALS (from visual inspection)
# =============================================================================

# Expected normal directions for each wall
# Based on polygon-based algorithm with CCW winding
# Format: wall_index -> (expected_x_sign, expected_y_sign)
# UP = (0, +1), DOWN = (0, -1), LEFT = (-1, 0), RIGHT = (+1, 0)
EXPECTED_NORMALS = {
    0: (0, -1),   # DOWN - bottom edge
    1: (1, 0),    # RIGHT
    2: (0, -1),   # DOWN
    3: (1, 0),    # RIGHT
    4: (0, -1),   # DOWN
    5: (1, 0),    # RIGHT
    6: (0, 1),    # UP - top edge of staircase
    7: (1, 0),    # RIGHT
    8: (0, 1),    # UP - top edge of staircase
    9: (1, 0),    # RIGHT - connects walls 8 and 10
    10: (0, 1),   # UP - top edge of staircase
    11: (-1, 0),  # LEFT
    12: (0, 1),   # UP - top edge of staircase
    13: (-1, 0),  # LEFT
    14: (0, -1),  # DOWN
    15: (-1, 0),  # LEFT
    16: (0, -1),  # DOWN
    17: (0, -1),  # DOWN
    18: (-1, 0),  # LEFT
}


# =============================================================================
# TESTS
# =============================================================================

class TestExtractCenterline:
    """Tests for centerline extraction."""
    
    def test_horizontal_wall(self):
        """Horizontal wall should have vertical normal."""
        # A horizontal wall (wider than tall)
        wall = WallPolygon(points=[
            Point(x=0, y=0),
            Point(x=100, y=0),
            Point(x=100, y=10),
            Point(x=0, y=10),
        ])
        seg = extract_centerline(wall)
        normal = seg.normal()
        
        # Should be mostly vertical
        assert abs(normal.y) > 0.9
    
    def test_vertical_wall(self):
        """Vertical wall should have horizontal normal."""
        # A vertical wall (taller than wide)
        wall = WallPolygon(points=[
            Point(x=0, y=0),
            Point(x=10, y=0),
            Point(x=10, y=100),
            Point(x=0, y=100),
        ])
        seg = extract_centerline(wall)
        normal = seg.normal()
        
        # Should be mostly horizontal
        assert abs(normal.x) > 0.9


class TestVisibility:
    """Tests for visibility algorithm - check expected walls per direction."""
    
    def test_back_view(self, real_walls):
        """BACK view should return walls facing up (back of building)."""
        visible = get_visible_wall_indices(real_walls, ViewDirection.BACK)
        expected = {6, 8, 10, 12}
        assert visible == expected, f"BACK: got {sorted(visible)}, expected {sorted(expected)}"
    
    def test_front_view(self, real_walls):
        """FRONT view should return walls facing down (front of building)."""
        visible = get_visible_wall_indices(real_walls, ViewDirection.FRONT)
        expected = {0, 2, 4, 14, 16, 17}
        assert visible == expected, f"FRONT: got {sorted(visible)}, expected {sorted(expected)}"
    
    def test_left_view(self, real_walls):
        """LEFT view should return walls facing left (on left side of building)."""
        visible = get_visible_wall_indices(real_walls, ViewDirection.LEFT)
        expected = {1, 3, 5, 7, 9, 15}
        assert visible == expected, f"LEFT: got {sorted(visible)}, expected {sorted(expected)}"
    
    def test_right_view(self, real_walls):
        """RIGHT view should return walls facing right (on right side of building)."""
        visible = get_visible_wall_indices(real_walls, ViewDirection.RIGHT)
        expected = {11, 13, 18}
        assert visible == expected, f"RIGHT: got {sorted(visible)}, expected {sorted(expected)}"
    
    def test_directions_are_disjoint(self, real_walls):
        """Walls visible from opposite directions should not overlap."""
        back = get_visible_wall_indices(real_walls, ViewDirection.BACK)
        front = get_visible_wall_indices(real_walls, ViewDirection.FRONT)
        left = get_visible_wall_indices(real_walls, ViewDirection.LEFT)
        right = get_visible_wall_indices(real_walls, ViewDirection.RIGHT)
        
        assert back.isdisjoint(front), f"BACK and FRONT overlap: {back & front}"
        assert left.isdisjoint(right), f"LEFT and RIGHT overlap: {left & right}"


class TestVector2D:
    """Tests for Vector2D operations."""
    
    def test_dot_product(self):
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        assert v1.dot(v2) == 0  # Perpendicular
        
        v3 = Vector2D(1, 0)
        assert v1.dot(v3) == 1  # Parallel
    
    def test_perpendicular_cw(self):
        v = Vector2D(1, 0)  # Right
        perp = v.perpendicular_cw()
        assert perp.x == 0
        assert perp.y == -1  # Down (CW from right)
    
    def test_normalize(self):
        v = Vector2D(3, 4)
        n = v.normalize()
        assert abs(n.x - 0.6) < 0.01
        assert abs(n.y - 0.8) < 0.01
