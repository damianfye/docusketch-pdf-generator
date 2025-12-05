"""Utility functions - pure helpers with no business logic."""

from utils.encoding import to_data_uri, svg_to_data_uri
from utils.geometry import normalize_coordinates

__all__ = [
    "to_data_uri",
    "svg_to_data_uri",
    "normalize_coordinates",
]
