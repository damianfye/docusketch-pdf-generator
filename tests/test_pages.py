"""Tests for page types and registry."""

import pytest

from pages.registry import PageRegistry
from pages.base import PageBase
from pages.windows_doors import WindowsDoorsPage
from models.document import PageConfig, PageMetadata
from models.table import TableData, TableRow
from models.primitives import Point, WallPolygon


class TestPageRegistry:
    """Tests for page registry."""
    
    def test_windows_doors_registered(self):
        """WindowsDoorsPage should be registered."""
        assert PageRegistry.is_registered("windows_doors")
    
    def test_get_registered_page(self):
        """Should return registered page class."""
        page_class = PageRegistry.get("windows_doors")
        
        assert page_class is WindowsDoorsPage
    
    def test_get_unknown_raises(self):
        """Should raise for unknown page type."""
        with pytest.raises(ValueError):
            PageRegistry.get("unknown_page_type")
    
    def test_list_types(self):
        """Should list all registered types."""
        types = PageRegistry.list_types()
        
        assert "windows_doors" in types


class TestWindowsDoorsPage:
    """Tests for WindowsDoorsPage."""
    
    def test_template_name(self):
        """Should return correct template name."""
        page = WindowsDoorsPage()
        
        assert page.template_name == "pages/windows_doors.html"
    
    def test_get_context_basic(self):
        """Should build context from config."""
        config = PageConfig(
            page_type="windows_doors",
            metadata=PageMetadata(
                title="Windows and Doors",
                document_id="Test123",
                address="123 Main St",
                section_name="Back",
            ),
        )
        
        page = WindowsDoorsPage()
        context = page.get_context(config, page_number=1)
        
        assert context["metadata"].title == "Windows and Doors"
        assert context["metadata"].document_id == "Test123"
        assert context["page_number"] == 1
    
    def test_get_context_with_table(self):
        """Should include table HTML when table_data provided."""
        config = PageConfig(
            page_type="windows_doors",
            metadata=PageMetadata(),
            table_data=TableData(
                rows=[
                    TableRow(wall="B1", window_door="W1", area_sqft=9.68, perimeter_ft=12.5, size="3x2"),
                ],
                total_count=1,
                total_area=9.68,
                total_perimeter=12.5,
            ),
        )
        
        page = WindowsDoorsPage()
        context = page.get_context(config)
        
        assert "table_html" in context
        assert "<table" in context["table_html"]
