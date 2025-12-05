"""Windows and Doors page type - the main page for this task."""

from pages.base import PageBase
from pages.registry import PageRegistry
from models.document import PageConfig
from renderers.svg import SVGRenderer
from renderers.image import ImageRenderer
from renderers.table import TableRenderer
from generators.floor_plan import FloorPlanGenerator


@PageRegistry.register("windows_doors")
class WindowsDoorsPage(PageBase):
    """
    Windows and Doors page type.
    
    This page displays:
    - Header with logo and document info
    - Section title ("Windows and Doors") and subsection ("Back")
    - Wall projection SVG (provided top.svg)
    - Floor plan SVG (generated from wall_data.json)
    - Panorama image
    - Data table with measurements
    - Footer with navigation
    """
    
    @property
    def template_name(self) -> str:
        return "pages/windows_doors.html"
    
    def get_context(self, config: PageConfig, **kwargs) -> dict:
        """
        Build context for the Windows and Doors template.
        
        Args:
            config: Page configuration
            **kwargs: Should include:
                - logo_svg: Main logo SVG string
                - logo_powered_png: Powered by logo bytes
                - page_number: Current page number
                
        Returns:
            Template context dictionary
        """
        context = {
            "metadata": config.metadata,
            "page_number": kwargs.get("page_number", 1),
        }
        
        # Logo (from kwargs, passed by DocumentGenerator)
        if "logo_svg" in kwargs:
            context["logo_svg"] = SVGRenderer(kwargs["logo_svg"]).render()
        
        # Powered by logo
        if "logo_powered_png" in kwargs:
            context["logo_powered_data_uri"] = ImageRenderer(
                kwargs["logo_powered_png"], 
                mime_type="image/png"
            ).render()
        
        # Wall projection SVG (provided, just embed)
        if config.wall_projection_svg:
            context["wall_projection_svg"] = SVGRenderer(
                config.wall_projection_svg
            ).render()
        
        # Floor plan SVG (GENERATED from wall data)
        if config.walls:
            floor_plan_svg = FloorPlanGenerator(
                walls=config.walls,
                width=300,
                height=220,
            ).generate()
            context["floor_plan_svg"] = floor_plan_svg
        
        # Panorama image
        if config.panorama_image:
            context["panorama_data_uri"] = ImageRenderer(
                config.panorama_image,
                mime_type="image/jpeg",
            ).render()
        
        # Data table
        if config.table_data:
            context["table_html"] = TableRenderer(config.table_data).render()
        
        return context
