"""Tests for the floor plan generator and boundary classification algorithm."""

import pytest

from models.primitives import Point, WallPolygon
from generators.floor_plan import FloorPlanGenerator
from utils.geometry import classify_boundary_walls, normalize_coordinates


class TestBoundaryClassification:
    """Tests for the wall boundary classification algorithm."""
    
    def test_empty_walls(self):
        """Empty input should return empty output."""
        result = classify_boundary_walls([])
        assert result == []
    
    def test_single_wall_is_boundary(self):
        """A single wall should be marked as boundary."""
        wall = WallPolygon(points=[
            Point(x=0, y=0),
            Point(x=10, y=0),
            Point(x=10, y=5),
            Point(x=0, y=5),
        ])
        
        result = classify_boundary_walls([wall])
        
        assert len(result) == 1
        assert result[0].is_boundary is True
    
    def test_square_all_boundary(self):
        """Four walls forming a square should all be boundaries."""
        # Create 4 walls forming a square
        walls = [
            # Top wall
            WallPolygon(points=[
                Point(x=0, y=0), Point(x=100, y=0),
                Point(x=100, y=5), Point(x=0, y=5),
            ]),
            # Right wall
            WallPolygon(points=[
                Point(x=95, y=0), Point(x=100, y=0),
                Point(x=100, y=100), Point(x=95, y=100),
            ]),
            # Bottom wall
            WallPolygon(points=[
                Point(x=0, y=95), Point(x=100, y=95),
                Point(x=100, y=100), Point(x=0, y=100),
            ]),
            # Left wall
            WallPolygon(points=[
                Point(x=0, y=0), Point(x=5, y=0),
                Point(x=5, y=100), Point(x=0, y=100),
            ]),
        ]
        
        result = classify_boundary_walls(walls)
        
        # All walls should be boundary walls
        assert all(w.is_boundary for w in result)


class TestCoordinateNormalization:
    """Tests for coordinate normalization."""
    
    def test_empty_walls(self):
        """Empty input should return empty output."""
        result = normalize_coordinates([], 200, 200)
        assert result == []
    
    def test_fits_within_viewport(self):
        """Normalized walls should fit within target viewport."""
        walls = [
            WallPolygon(points=[
                Point(x=1000, y=1000),
                Point(x=2000, y=1000),
                Point(x=2000, y=1500),
                Point(x=1000, y=1500),
            ])
        ]
        
        result = normalize_coordinates(walls, 200, 200, padding=10)
        
        # All points should be within viewport (with padding)
        for wall in result:
            for point in wall.points:
                assert 10 <= point.x <= 190
                assert 10 <= point.y <= 190


class TestFloorPlanGenerator:
    """Tests for the floor plan SVG generator."""
    
    def test_generates_svg(self):
        """Generator should produce valid SVG string."""
        walls = [
            WallPolygon(points=[
                Point(x=0, y=0),
                Point(x=100, y=0),
                Point(x=100, y=100),
                Point(x=0, y=100),
            ])
        ]
        
        generator = FloorPlanGenerator(walls, width=200, height=200)
        svg = generator.generate()
        
        assert svg.startswith("<svg")
        assert "viewBox" in svg
        assert "<polygon" in svg
    
    def test_empty_walls_placeholder(self):
        """Empty walls should produce placeholder SVG."""
        generator = FloorPlanGenerator([], width=200, height=200)
        svg = generator.generate()
        
        assert "<svg" in svg
        assert "No floor plan data" in svg
