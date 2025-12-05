"""Document generator - main orchestrator."""

from pathlib import Path

from models.document import DocumentConfig, PageConfig
from pages.registry import PageRegistry
from core.template_engine import TemplateEngine
from core.pdf_renderer import PDFRenderer


class DocumentGenerator:
    """
    Main entry point for PDF generation.
    
    Orchestrates:
    1. Loading page types from registry
    2. Rendering each page to HTML
    3. Combining pages into final document
    4. Converting to PDF via WeasyPrint
    """
    
    def __init__(
        self,
        templates_dir: Path | str | None = None,
        styles_dir: Path | str | None = None,
    ):
        """
        Initialize document generator.
        
        Args:
            templates_dir: Path to templates (default: ./templates)
            styles_dir: Path to SCSS styles (default: ./styles)
        """
        # Default paths relative to project root
        project_root = Path(__file__).parent.parent
        
        self.templates_dir = Path(templates_dir) if templates_dir else project_root / "templates"
        self.styles_dir = Path(styles_dir) if styles_dir else project_root / "styles"
        
        # Initialize engines
        self.template_engine = TemplateEngine(self.templates_dir, self.styles_dir)
        self.pdf_renderer = PDFRenderer(base_url=str(project_root))
    
    def generate(self, config: DocumentConfig) -> bytes:
        """
        Generate PDF from document configuration.
        
        Args:
            config: Document configuration with pages and assets
            
        Returns:
            PDF file as bytes
        """
        # Render all pages to HTML
        pages_html = []
        
        for page_num, page_config in enumerate(config.pages, start=1):
            page_html = self._render_page(
                page_config,
                logo_svg=config.logo_svg,
                logo_powered_png=config.logo_powered_png,
                page_number=page_num,
            )
            pages_html.append(page_html)
        
        # Combine into single document
        # For multi-page, we'd use CSS page breaks
        # For now, just concatenate (single page task)
        full_html = self._combine_pages(pages_html)
        
        # Convert to PDF
        return self.pdf_renderer.render(full_html)
    
    def _render_page(
        self,
        page_config: PageConfig,
        **kwargs,
    ) -> str:
        """
        Render a single page to HTML.
        
        Args:
            page_config: Page configuration
            **kwargs: Additional context (logos, page number)
            
        Returns:
            Rendered HTML string
        """
        # Get page type from registry
        page_class = PageRegistry.get(page_config.page_type)
        page = page_class()
        
        # Build context
        context = page.get_context(page_config, **kwargs)
        
        # Render template
        return self.template_engine.render(page.template_name, context)
    
    def _combine_pages(self, pages_html: list[str]) -> str:
        """
        Combine multiple page HTMLs into single document.
        
        For now, just returns the first page (single page task).
        For multi-page, would add page breaks.
        
        Args:
            pages_html: List of rendered page HTML strings
            
        Returns:
            Combined HTML document
        """
        if not pages_html:
            return "<html><body>No pages</body></html>"
        
        # For single page, just return it
        # TODO: For multi-page, wrap with page breaks
        return pages_html[0]
