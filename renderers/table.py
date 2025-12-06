"""Table renderer."""

from __future__ import annotations

from renderers.base import RendererBase
from models.table import TableData


class TableRenderer(RendererBase):
    """Renders TableData as an HTML table."""
    
    def __init__(self, data: TableData):
        self.data = data
    
    def render(self) -> str:
        """Generate HTML table string."""
        rows_html = []
        
        # Header row
        rows_html.append("""
            <tr class="header-row">
                <th>Wall</th>
                <th>Window/Door</th>
                <th>Area, ft²</th>
                <th>Perimeter, ft</th>
                <th>Size (WxH), ft</th>
            </tr>
        """)
        
        # Data rows
        for i, row in enumerate(self.data.rows):
            row_class = "data-row-odd" if i % 2 == 0 else "data-row-even"
            rows_html.append(f"""
                <tr class="{row_class}">
                    <td>{row.wall or ""}</td>
                    <td>{row.window_door}</td>
                    <td>{row.area_sqft:.2f}</td>
                    <td>{row.perimeter_ft:.2f}</td>
                    <td>{row.size}</td>
                </tr>
            """)
        
        # Total row
        rows_html.append(f"""
            <tr class="total-row">
                <td>Total</td>
                <td>{self.data.total_count}</td>
                <td>{self.data.total_area:.2f}</td>
                <td>{self.data.total_perimeter:.2f}</td>
                <td>--</td>
            </tr>
        """)
        
        return f"""
            <table class="data-table">
                {"".join(rows_html)}
            </table>
        """
