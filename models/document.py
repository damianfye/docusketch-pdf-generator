"""Document configuration models."""

from __future__ import annotations

from pydantic import BaseModel

from models.primitives import WallPolygon
from models.table import TableData
from generators.visibility import ViewDirection


class PageMetadata(BaseModel):
    """Metadata displayed in page header."""
    title: str = "Windows and Doors"
    document_id: str = "Test"
    address: str = "127 Example St, Sample City, CA 90210"
    section_name: str = "Back"


class PageConfig(BaseModel):
    """Configuration for a single page."""
    page_type: str
    metadata: PageMetadata
    table_data: TableData | None = None
    walls: list[WallPolygon] | None = None
    view_direction: ViewDirection = ViewDirection.BACK
    wall_projection_svg: str | None = None
    panorama_image: bytes | None = None


class DocumentConfig(BaseModel):
    """Configuration for the entire document."""
    pages: list[PageConfig]
    logo_svg: str
    logo_powered_png: bytes
