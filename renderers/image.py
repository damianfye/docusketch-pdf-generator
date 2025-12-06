"""Image renderer."""

from __future__ import annotations

from pathlib import Path

from renderers.base import RendererBase
from utils.encoding import to_data_uri


class ImageRenderer(RendererBase):
    """Renders image bytes as a data URI for embedding in HTML."""
    
    def __init__(self, image_bytes: bytes, mime_type: str = "image/jpeg"):
        self.image_bytes = image_bytes
        self.mime_type = mime_type
    
    def render(self) -> str:
        """Convert image to data URI."""
        return to_data_uri(self.image_bytes, self.mime_type)
    
    @classmethod
    def from_file(cls, filepath: str) -> ImageRenderer:
        """Create renderer from file path."""
        path = Path(filepath)
        image_bytes = path.read_bytes()
        
        # Infer MIME type from extension
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
        }
        mime_type = mime_map.get(path.suffix.lower(), "image/jpeg")
        
        return cls(image_bytes, mime_type)
