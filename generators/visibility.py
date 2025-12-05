"""
Wall Visibility Algorithm

Determines which walls are visible from orthographic viewing directions.
Uses normal vectors and dot product - works for any wall angle.

This is THE ALGORITHM the interview task asks for.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.primitives import WallPolygon


# =============================================================================
# DATA TYPES
# =============================================================================

class ViewDirection(Enum):
    """Orthographic viewing directions for floor plan."""
    BACK = "back"      # Looking at back of building (top edge in SVG)
    FRONT = "front"    # Looking at front of building (bottom edge in SVG)
    LEFT = "left"      # Looking at left side of building
    RIGHT = "right"    # Looking at right side of building
    
    # Aliases for backward compatibility
    TOP = "back"
    BOTTOM = "front"


@dataclass
class Vector2D:
    """2D vector for geometric calculations."""
    x: float
    y: float
    
    def dot(self, other: Vector2D) -> float:
        """Dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def normalize(self) -> Vector2D:
        """Return unit vector in same direction."""
        magnitude = (self.x ** 2 + self.y ** 2) ** 0.5
        if magnitude == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / magnitude, self.y / magnitude)
    
    def perpendicular_cw(self) -> Vector2D:
        """Return perpendicular vector (rotated 90° clockwise)."""
        # CW rotation: (x, y) -> (y, -x)
        # For our polygon traversal, this gives outward-pointing normal
        return Vector2D(self.y, -self.x)


@dataclass
class Segment:
    """Line segment defined by start and end points."""
    start: Vector2D
    end: Vector2D
    
    def direction(self) -> Vector2D:
        """Get direction vector from start to end."""
        return Vector2D(self.end.x - self.start.x, self.end.y - self.start.y)
    
    def normal(self) -> Vector2D:
        """
        Get outward-pointing normal vector.
        
        For our polygon traversal, 90° CW gives outward normal.
        """
        return self.direction().perpendicular_cw().normalize()


# =============================================================================
# VIEW DIRECTION MAPPING
# =============================================================================

def get_view_vector(direction: ViewDirection | str) -> Vector2D:
    """
    Convert viewing direction to unit vector.
    
    View vectors point FROM the viewer TOWARD the scene.
    Uses SVG coordinates (Y increases downward):
    - TOP: viewer above (low Y), looking down → (0, +1)
    - BOTTOM: viewer below (high Y), looking up → (0, -1)
    - LEFT: viewer on left, looking right → (+1, 0)
    - RIGHT: viewer on right, looking left → (-1, 0)
    
    For backface culling: wall visible if normal · view_vector < 0
    (normal points outward from building, view points toward scene)
    """
    if isinstance(direction, str):
        direction = ViewDirection(direction.lower())
    
    # SVG coords: Y increases downward
    # BACK/FRONT refer to building orientation, not viewer position
    vectors = {
        ViewDirection.BACK: Vector2D(0, 1),     # Back walls face up (low Y), view toward high Y
        ViewDirection.FRONT: Vector2D(0, -1),   # Front walls face down (high Y), view toward low Y
        ViewDirection.LEFT: Vector2D(1, 0),     # Left walls face left, view toward right
        ViewDirection.RIGHT: Vector2D(-1, 0),   # Right walls face right, view toward left
    }
    return vectors.get(direction, vectors[ViewDirection.BACK])


# =============================================================================
# SEGMENT EXTRACTION
# =============================================================================

def get_short_edge_midpoints(wall: WallPolygon) -> tuple[Vector2D, Vector2D]:
    """
    Get midpoints of the two short edges of a wall rectangle.
    
    Args:
        wall: 4-point wall polygon
        
    Returns:
        Tuple of two midpoints (as Vector2D)
    """
    points = wall.points
    if len(points) != 4:
        raise ValueError(f"Wall must have 4 points, got {len(points)}")
    
    # Calculate edge lengths
    edges = []
    for i in range(4):
        p1 = points[i]
        p2 = points[(i + 1) % 4]
        length = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
        mid = Vector2D((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        edges.append((length, mid))
    
    # Sort by length, return two shortest (the "ends" of the wall)
    edges.sort(key=lambda e: e[0])
    return edges[0][1], edges[1][1]


def build_polygon_vertices(walls: list[WallPolygon]) -> list[Vector2D]:
    """
    Build polygon vertices from wall rectangles.
    
    Each wall contributes one edge to the polygon. Adjacent walls
    share a vertex (the overlapping short-edge midpoint).
    
    Edge i (vertex[i] → vertex[i+1]) corresponds to wall i.
    
    Args:
        walls: List of wall polygons in order
        
    Returns:
        List of n vertices forming the building outline polygon
    """
    if not walls:
        return []
    
    n = len(walls)
    
    def points_equal(p1: Vector2D, p2: Vector2D, tol: float = 1.0) -> bool:
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5 < tol
    
    def get_shared_midpoint(wall_a: WallPolygon, wall_b: WallPolygon) -> Vector2D:
        """Find the midpoint shared between two adjacent walls."""
        mids_a = get_short_edge_midpoints(wall_a)
        mids_b = get_short_edge_midpoints(wall_b)
        
        for ma in mids_a:
            for mb in mids_b:
                if points_equal(ma, mb):
                    return ma
        
        # Fallback: return first midpoint of wall_a
        return mids_a[0]
    
    # Build vertices: vertex[i] is the shared point between wall[i-1] and wall[i]
    # So edge i (vertex[i] → vertex[i+1]) spans wall[i]
    vertices = []
    for i in range(n):
        prev_wall = walls[(i - 1) % n]
        curr_wall = walls[i]
        shared = get_shared_midpoint(prev_wall, curr_wall)
        vertices.append(shared)
    
    return vertices


def extract_centerline(wall: WallPolygon) -> Segment:
    """
    Extract centerline segment from a wall polygon.
    
    A wall polygon is a thick rectangle (4 points). The centerline
    connects the midpoints of the two short edges.
    
    Note: For visibility calculations, prefer build_polygon_vertices()
    which correctly handles the polygon winding order.
    
    Args:
        wall: 4-point wall polygon
        
    Returns:
        Segment representing the wall's centerline
    """
    mid_a, mid_b = get_short_edge_midpoints(wall)
    return Segment(start=mid_a, end=mid_b)


def _legacy_extract_centerline(wall: WallPolygon) -> Segment:
    """Legacy centerline extraction (kept for reference)."""
    points = wall.points
    if len(points) != 4:
        raise ValueError(f"Wall must have 4 points, got {len(points)}")
    
    edges = []
    for i in range(4):
        p1 = points[i]
        p2 = points[(i + 1) % 4]
        length = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
        edges.append((i, length, p1, p2))
    
    # Find the two short edges (ends of wall rectangle)
    # They are opposite edges: either (0,2) or (1,3)
    len_01 = edges[0][1]
    len_12 = edges[1][1]
    
    if len_01 < len_12:
        # Edges 0 and 2 are short (ends), edges 1 and 3 are long (sides)
        # Centerline goes from midpoint of edge 0 to midpoint of edge 2
        # This preserves CCW winding: edge 0 -> edge 1 -> edge 2
        short_edge_first = edges[0]
        short_edge_second = edges[2]
    else:
        # Edges 1 and 3 are short (ends), edges 0 and 2 are long (sides)
        # Centerline goes from midpoint of edge 1 to midpoint of edge 3
        short_edge_first = edges[1]
        short_edge_second = edges[3]
    
    # Midpoint of first short edge (start of centerline)
    mid1 = Vector2D(
        (short_edge_first[2].x + short_edge_first[3].x) / 2,
        (short_edge_first[2].y + short_edge_first[3].y) / 2,
    )
    # Midpoint of second short edge (end of centerline)
    mid2 = Vector2D(
        (short_edge_second[2].x + short_edge_second[3].x) / 2,
        (short_edge_second[2].y + short_edge_second[3].y) / 2,
    )
    
    return Segment(start=mid1, end=mid2)


# =============================================================================
# VISIBILITY ALGORITHM
# =============================================================================

def is_segment_visible(
    segment: Segment,
    view_vector: Vector2D,
    outward_normal: Vector2D,
) -> bool:
    """
    Check if a segment is visible from a viewing direction.
    
    Uses backface culling: visible if outward normal faces the viewer.
    
    Args:
        segment: Line segment (used for context, not calculation)
        view_vector: Unit vector pointing FROM viewer TOWARD scene
        outward_normal: Pre-computed outward-pointing normal
        
    Returns:
        True if segment faces the viewer
    """
    # Visible when normal points OPPOSITE to view direction
    # (normal toward viewer, view_vector away from viewer)
    # dot(normal, view_vector) < 0 means they point opposite ways
    # Use epsilon to avoid floating point issues with perpendicular walls
    EPSILON = 1e-6
    return outward_normal.dot(view_vector) < -EPSILON


def compute_building_centroid(walls: list[WallPolygon]) -> Vector2D:
    """
    Compute the centroid of all wall points.
    
    Used to determine "outward" direction for normals.
    """
    all_x = []
    all_y = []
    for wall in walls:
        for p in wall.points:
            all_x.append(p.x)
            all_y.append(p.y)
    
    return Vector2D(
        sum(all_x) / len(all_x),
        sum(all_y) / len(all_y),
    )


def get_outward_normal(segment: Segment, centroid: Vector2D) -> Vector2D:
    """
    Get the outward-pointing normal for a segment.
    
    Computes perpendicular, then flips if it points toward centroid.
    This handles inconsistent winding order in the data.
    
    Args:
        segment: Wall centerline segment
        centroid: Building centroid (interior point)
        
    Returns:
        Unit normal pointing away from building interior
    """
    # Get perpendicular (could point either way)
    normal = segment.normal()
    
    # Segment midpoint
    mid = Vector2D(
        (segment.start.x + segment.end.x) / 2,
        (segment.start.y + segment.end.y) / 2,
    )
    
    # Vector from midpoint toward centroid
    to_centroid = Vector2D(
        centroid.x - mid.x,
        centroid.y - mid.y,
    )
    
    # If normal points toward centroid, flip it
    if normal.dot(to_centroid) > 0:
        normal = Vector2D(-normal.x, -normal.y)
    
    return normal


def get_visible_wall_indices(
    walls: list[WallPolygon],
    direction: ViewDirection | str,
) -> set[int]:
    """
    Main API: Find which walls are visible from a viewing direction.
    
    Algorithm:
    1. Build polygon from wall midpoints (each wall = one edge)
    2. For each edge, compute outward normal (90° CCW from direction)
    3. Wall is visible if normal faces the viewer (dot product < 0)
    
    Args:
        walls: List of wall polygons forming building outline
        direction: Viewing direction (top/bottom/left/right)
        
    Returns:
        Set of wall indices that are visible
    """
    if not walls or len(walls) < 2:
        return set()
    
    if isinstance(direction, str):
        direction = ViewDirection(direction.lower())
    
    view_vector = get_view_vector(direction)
    
    # Build polygon vertices from wall midpoints
    vertices = build_polygon_vertices(walls)
    n = len(vertices)
    
    visible = set()
    
    # Each edge i (from vertex[i] to vertex[i+1]) corresponds to wall i
    for i in range(n):
        v_start = vertices[i]
        v_end = vertices[(i + 1) % n]
        
        # Edge direction
        edge_dir = Vector2D(v_end.x - v_start.x, v_end.y - v_start.y)
        
        # Outward normal = 90° CW from edge direction
        normal = edge_dir.perpendicular_cw().normalize()
        
        # Visible if normal points opposite to view direction
        # Use epsilon to avoid floating point issues
        EPSILON = 1e-6
        if normal.dot(view_vector) < -EPSILON:
            visible.add(i)
    
    return visible


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def classify_walls_by_visibility(
    walls: list[WallPolygon],
    direction: ViewDirection | str,
) -> list[WallPolygon]:
    """
    Return walls with is_boundary flag set based on visibility.
    
    Args:
        walls: List of wall polygons
        direction: Viewing direction
        
    Returns:
        New list of WallPolygon with is_boundary=True for visible walls
    """
    visible_indices = get_visible_wall_indices(walls, direction)
    
    result = []
    for i, wall in enumerate(walls):
        is_visible = i in visible_indices
        result.append(wall.model_copy_with_boundary(is_visible))
    
    return result
