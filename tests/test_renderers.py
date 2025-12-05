"""Tests for renderers."""

import pytest

from models.table import TableRow, TableData
from renderers.svg import SVGRenderer
from renderers.image import ImageRenderer
from renderers.table import TableRenderer


class TestSVGRenderer:
    """Tests for SVG renderer."""
    
    def test_renders_valid_svg(self):
        """Should return SVG content unchanged."""
        svg = '<svg viewBox="0 0 100 100"><rect /></svg>'
        renderer = SVGRenderer(svg)
        
        result = renderer.render()
        
        assert result == svg
    
    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        svg = '  <svg></svg>  '
        renderer = SVGRenderer(svg)
        
        result = renderer.render()
        
        assert result == '<svg></svg>'
    
    def test_rejects_invalid_svg(self):
        """Should raise error for non-SVG content."""
        renderer = SVGRenderer('<div>not svg</div>')
        
        with pytest.raises(ValueError):
            renderer.render()


class TestImageRenderer:
    """Tests for image renderer."""
    
    def test_renders_data_uri(self):
        """Should produce valid data URI."""
        image_bytes = b'\x89PNG\r\n\x1a\n'  # PNG header
        renderer = ImageRenderer(image_bytes, mime_type="image/png")
        
        result = renderer.render()
        
        assert result.startswith("data:image/png;base64,")
    
    def test_default_mime_type(self):
        """Should default to JPEG mime type."""
        renderer = ImageRenderer(b'test')
        
        result = renderer.render()
        
        assert "image/jpeg" in result


class TestTableRenderer:
    """Tests for table renderer."""
    
    def test_renders_html_table(self):
        """Should produce HTML table."""
        data = TableData(
            rows=[
                TableRow(wall="B1", window_door="W1", area_sqft=9.68, perimeter_ft=12.5, size="3.42 x 2.83"),
            ],
            total_count=1,
            total_area=9.68,
            total_perimeter=12.5,
        )
        renderer = TableRenderer(data)
        
        result = renderer.render()
        
        assert "<table" in result
        assert "B1" in result
        assert "W1" in result
        assert "9.68" in result
        assert "Total" in result
