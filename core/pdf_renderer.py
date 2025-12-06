"""PDF renderer - WeasyPrint wrapper."""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

from weasyprint import HTML, CSS


class PDFRenderer:
    """PDF renderer using WeasyPrint."""
    
    def __init__(self, base_url: str | Path | None = None):
        self.base_url = str(base_url) if base_url else None
    
    def render(self, html_content: str, extra_css: str | None = None) -> bytes:
        """Render HTML to PDF bytes."""
        # Create HTML document
        html = HTML(string=html_content, base_url=self.base_url)
        
        # Prepare stylesheets
        stylesheets = []
        if extra_css:
            stylesheets.append(CSS(string=extra_css))
        
        # Render to PDF
        pdf_bytes = html.write_pdf(stylesheets=stylesheets or None)
        
        return pdf_bytes
    
    def render_to_file(
        self, 
        html_content: str, 
        output_path: Path | str,
        extra_css: str | None = None,
    ) -> None:
        """Render HTML to PDF file."""
        pdf_bytes = self.render(html_content, extra_css)
        
        output_path = Path(output_path)
        output_path.write_bytes(pdf_bytes)
