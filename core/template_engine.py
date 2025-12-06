"""Template engine - Jinja2 + SCSS compilation."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils.scss import compile_scss


class TemplateEngine:
    """Template engine combining Jinja2 templates with SCSS styles."""
    
    def __init__(
        self,
        templates_dir: Path | str,
        styles_dir: Path | str,
    ):
        self.templates_dir = Path(templates_dir)
        self.styles_dir = Path(styles_dir)
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        
        # Cache compiled CSS
        self._css_cache: str | None = None
    
    def get_css(self) -> str:
        """Get compiled CSS from SCSS."""
        if self._css_cache is None:
            main_scss = self.styles_dir / "main.scss"
            if main_scss.exists():
                self._css_cache = compile_scss(main_scss)
            else:
                self._css_cache = ""
        return self._css_cache
    
    def render(self, template_name: str, context: dict) -> str:
        """Render a template with context."""
        template = self.env.get_template(template_name)
        
        # Inject CSS into context
        full_context = {
            "css": self.get_css(),
            **context,
        }
        
        return template.render(**full_context)
    
    def render_string(self, template_string: str, context: dict) -> str:
        """Render a template from string."""
        template = self.env.from_string(template_string)
        return template.render(**context)
