"""Primitive data types - the atomic building blocks."""

from pydantic import BaseModel


class Point(BaseModel):
    """2D coordinate - the atomic primitive."""
    x: float
    y: float
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class WallPolygon(BaseModel):
    """
    A wall represented as a polygon (4 corner points).
    
    Attributes:
        points: List of 4 corner points defining the wall rectangle
        is_boundary: Whether this wall is on the exterior boundary (set by algorithm)
    """
    points: list[Point]
    is_boundary: bool = False
    
    @property
    def center(self) -> Point:
        """Calculate the center point of the wall."""
        avg_x = sum(p.x for p in self.points) / len(self.points)
        avg_y = sum(p.y for p in self.points) / len(self.points)
        return Point(x=avg_x, y=avg_y)
    
    def model_copy_with_boundary(self, is_boundary: bool) -> "WallPolygon":
        """Return a copy with updated boundary flag."""
        return WallPolygon(points=self.points, is_boundary=is_boundary)
