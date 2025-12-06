"""SVG renderer."""

from __future__ import annotations

from renderers.base import RendererBase


class SVGRenderer(RendererBase):
    """Renders SVG content for embedding in HTML."""
    
    def __init__(self, svg_content: str, width: str | None = None, height: str | None = None):
        self.svg_content = svg_content
        self.width = width
        self.height = height
    
    def render(self) -> str:
        """Return cleaned SVG ready for embedding."""
        svg = self.svg_content.strip()
        
        # Basic validation - ensure it's SVG
        if not svg.startswith("<svg") and not svg.startswith("<?xml"):
            raise ValueError("Invalid SVG content")
        
        # Could add more processing here:
        # - Remove XML declaration if present
        # - Adjust viewBox
        # - Override width/height
        
        return svg
