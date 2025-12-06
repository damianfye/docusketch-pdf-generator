"""Primitive data types."""

from __future__ import annotations

from pydantic import BaseModel


class Point(BaseModel):
    """2D coordinate - the atomic primitive."""
    x: float
    y: float
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class WallPolygon(BaseModel):
    """A wall represented as a 4-point polygon."""
    points: list[Point]
    is_boundary: bool = False
    
    @property
    def center(self) -> Point:
        """Center point of the wall."""
        avg_x = sum(p.x for p in self.points) / len(self.points)
        avg_y = sum(p.y for p in self.points) / len(self.points)
        return Point(x=avg_x, y=avg_y)
    
    def model_copy_with_boundary(self, is_boundary: bool) -> WallPolygon:
        """Copy with updated boundary flag."""
        return WallPolygon(points=self.points, is_boundary=is_boundary)
