"""Table data models."""

from __future__ import annotations

from pydantic import BaseModel


class TableRow(BaseModel):
    """Single row in the measurement table."""
    wall: str | None = None  # "B1", "B2", etc. or None
    window_door: str         # "W1", "W2", etc.
    area_sqft: float
    perimeter_ft: float
    size: str                # "3.42 x 2.83"


class TableData(BaseModel):
    """Table data with rows and computed totals."""
    rows: list[TableRow]
    total_count: int
    total_area: float
    total_perimeter: float
    
    @classmethod
    def from_rows(cls, rows: list[TableRow]) -> TableData:
        """Create with computed totals."""
        return cls(
            rows=rows,
            total_count=len(rows),
            total_area=sum(r.area_sqft for r in rows),
            total_perimeter=sum(r.perimeter_ft for r in rows),
        )
