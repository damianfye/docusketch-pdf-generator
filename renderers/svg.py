"""SVG renderer - embeds and cleans SVG strings."""

from renderers.base import RendererBase


class SVGRenderer(RendererBase):
    """
    Renders SVG content for embedding in HTML.
    
    Takes an existing SVG string and prepares it for embedding.
    Can optionally clean/validate the SVG.
    """
    
    def __init__(self, svg_content: str, width: str | None = None, height: str | None = None):
        """
        Initialize SVG renderer.
        
        Args:
            svg_content: Raw SVG string
            width: Optional width override
            height: Optional height override
        """
        self.svg_content = svg_content
        self.width = width
        self.height = height
    
    def render(self) -> str:
        """
        Return cleaned SVG ready for embedding.
        
        Returns:
            SVG string
        """
        svg = self.svg_content.strip()
        
        # Basic validation - ensure it's SVG
        if not svg.startswith("<svg") and not svg.startswith("<?xml"):
            raise ValueError("Invalid SVG content")
        
        # Could add more processing here:
        # - Remove XML declaration if present
        # - Adjust viewBox
        # - Override width/height
        
        return svg
