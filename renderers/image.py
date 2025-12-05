"""Image renderer - converts images to data URIs."""

from renderers.base import RendererBase
from utils.encoding import to_data_uri


class ImageRenderer(RendererBase):
    """
    Renders image bytes as a data URI for embedding in HTML.
    
    Converts raw image bytes to base64-encoded data URI.
    """
    
    def __init__(self, image_bytes: bytes, mime_type: str = "image/jpeg"):
        """
        Initialize image renderer.
        
        Args:
            image_bytes: Raw image bytes
            mime_type: MIME type of the image (default: image/jpeg)
        """
        self.image_bytes = image_bytes
        self.mime_type = mime_type
    
    def render(self) -> str:
        """
        Convert image to data URI.
        
        Returns:
            Data URI string (e.g., "data:image/jpeg;base64,...")
        """
        return to_data_uri(self.image_bytes, self.mime_type)
    
    @classmethod
    def from_file(cls, filepath: str) -> "ImageRenderer":
        """
        Create renderer from file path.
        
        Args:
            filepath: Path to image file
            
        Returns:
            ImageRenderer instance
        """
        from pathlib import Path
        
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
