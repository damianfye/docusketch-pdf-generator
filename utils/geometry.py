"""Geometry utilities for coordinate transformations."""

from models.primitives import Point, WallPolygon


def normalize_coordinates(
    walls: list[WallPolygon],
    target_width: float,
    target_height: float,
    padding: float = 10.0,
) -> list[WallPolygon]:
    """
    Scale and translate wall coordinates to fit within target viewport.
    
    Args:
        walls: List of wall polygons with original coordinates
        target_width: Target viewport width
        target_height: Target viewport height
        padding: Padding around the edges
        
    Returns:
        New list of WallPolygon with normalized coordinates
    """
    if not walls:
        return []
    
    # Find bounding box of all points
    all_x = [p.x for w in walls for p in w.points]
    all_y = [p.y for w in walls for p in w.points]
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    # Calculate scale to fit within target (minus padding)
    data_width = max_x - min_x
    data_height = max_y - min_y
    
    if data_width == 0 or data_height == 0:
        return walls
    
    available_width = target_width - 2 * padding
    available_height = target_height - 2 * padding
    
    scale = min(available_width / data_width, available_height / data_height)
    
    # Transform each wall
    normalized = []
    for wall in walls:
        new_points = []
        for p in wall.points:
            new_x = padding + (p.x - min_x) * scale
            new_y = padding + (p.y - min_y) * scale
            new_points.append(Point(x=new_x, y=new_y))
        
        normalized.append(WallPolygon(
            points=new_points,
            is_boundary=wall.is_boundary,
        ))
    
    return normalized


