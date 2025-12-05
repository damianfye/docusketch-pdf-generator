"""Document configuration models."""

from pydantic import BaseModel

from models.primitives import WallPolygon
from models.table import TableData


class PageMetadata(BaseModel):
    """Metadata displayed in page header."""
    title: str = "Windows and Doors"
    document_id: str = "Test"
    address: str = "127 Example St, Sample City, CA 90210"
    section_name: str = "Back"


class PageConfig(BaseModel):
    """
    Configuration for a single page.
    
    Attributes:
        page_type: Type of page (e.g., "windows_doors", "cover")
        metadata: Header/title information
        table_data: Measurement table data (optional for some page types)
        walls: Wall polygons for floor plan generation (optional)
        wall_projection_svg: Provided SVG for wall projection (top.svg)
        panorama_image: 360° panorama image bytes
    """
    page_type: str
    metadata: PageMetadata
    table_data: TableData | None = None
    walls: list[WallPolygon] | None = None
    wall_projection_svg: str | None = None
    panorama_image: bytes | None = None


class DocumentConfig(BaseModel):
    """
    Configuration for the entire document.
    
    Attributes:
        pages: List of page configurations
        logo_svg: Main DocuSketch logo SVG string
        logo_powered_png: "Powered by DocuSketch" logo bytes
    """
    pages: list[PageConfig]
    logo_svg: str
    logo_powered_png: bytes
