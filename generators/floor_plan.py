"""Floor plan generator.

Generates 2D floor plan SVG from wall polygon data.
Uses visibility algorithm to determine which walls to highlight.
"""

from __future__ import annotations

from models.primitives import WallPolygon
from utils.geometry import normalize_coordinates
from generators.visibility import (
    ViewDirection,
    classify_walls_by_visibility,
)


class FloorPlanGenerator:
    """Generates 2D floor plan SVG from wall polygons."""
    
    # Default colors matching DocuSketch style - NO STROKE (walls are thin)
    HIGHLIGHT_COLOR = "#61A5D8"  # Blue for visible/back walls
    DEFAULT_COLOR = "#000000"    # Black for other walls
    
    def __init__(
        self,
        walls: list[WallPolygon],
        view_direction: ViewDirection | str = ViewDirection.BACK,
        width: float = 200,
        height: float = 200,
        highlight_color: str | None = None,
        default_color: str | None = None,
    ):
        self.walls = walls
        self.view_direction = view_direction
        self.width = width
        self.height = height
        self.highlight_color = highlight_color or self.HIGHLIGHT_COLOR
        self.default_color = default_color or self.DEFAULT_COLOR
    
    def generate(self) -> str:
        """Generate SVG string for the floor plan."""
        if not self.walls:
            return self._empty_svg()
        
        # Step 1: Classify walls by visibility (THE ALGORITHM)
        classified_walls = classify_walls_by_visibility(
            self.walls,
            self.view_direction,
        )
        
        # Step 2: Normalize coordinates to fit viewport
        normalized_walls = normalize_coordinates(
            classified_walls,
            self.width,
            self.height,
            padding=10.0,
        )
        
        # Step 3: Generate SVG
        return self._generate_svg(normalized_walls)
    
    def _generate_svg(self, walls: list[WallPolygon]) -> str:
        """Generate SVG from processed walls."""
        polygons = []
        
        for wall in walls:
            # Choose color based on visibility
            fill_color = self.highlight_color if wall.is_boundary else self.default_color
            
            # Generate points string for polygon
            points_str = " ".join(f"{p.x:.2f},{p.y:.2f}" for p in wall.points)
            
            # Use stroke same as fill to make walls thicker
            polygon = f'<polygon points="{points_str}" fill="{fill_color}" stroke="{fill_color}" stroke-width="1.5"/>'
            polygons.append(polygon)
        
        return f'''<svg 
            viewBox="0 0 {self.width} {self.height}" 
            xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="xMidYMid meet"
        >
            {"".join(polygons)}
        </svg>'''
    
    def _empty_svg(self) -> str:
        """Return an empty SVG placeholder."""
        return f'''<svg 
            viewBox="0 0 {self.width} {self.height}" 
            xmlns="http://www.w3.org/2000/svg"
        >
            <text x="50%" y="50%" text-anchor="middle" fill="#999">
                No floor plan data
            </text>
        </svg>'''
