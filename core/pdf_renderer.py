"""PDF renderer - WeasyPrint wrapper."""

from pathlib import Path
from io import BytesIO

from weasyprint import HTML, CSS


class PDFRenderer:
    """
    PDF renderer using WeasyPrint.
    
    Converts HTML string to PDF bytes.
    """
    
    def __init__(self, base_url: str | Path | None = None):
        """
        Initialize PDF renderer.
        
        Args:
            base_url: Base URL for resolving relative paths in HTML
        """
        self.base_url = str(base_url) if base_url else None
    
    def render(self, html_content: str, extra_css: str | None = None) -> bytes:
        """
        Render HTML to PDF.
        
        Args:
            html_content: Complete HTML document string
            extra_css: Optional additional CSS to apply
            
        Returns:
            PDF file as bytes
        """
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
        """
        Render HTML to PDF file.
        
        Args:
            html_content: Complete HTML document string
            output_path: Path to save PDF file
            extra_css: Optional additional CSS to apply
        """
        pdf_bytes = self.render(html_content, extra_css)
        
        output_path = Path(output_path)
        output_path.write_bytes(pdf_bytes)
