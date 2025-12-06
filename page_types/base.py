"""Base class for page types."""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.document import PageConfig


class PageBase(ABC):
    """
    Abstract base for page types.
    
    A page is responsible for:
    1. Knowing which template to use (base.html vs base_minimal.html)
    2. Knowing which renderers/generators to call for its blocks
    3. Assembling the context for its template
    
    Each page type is a plugin that can be registered with PageRegistry.
    """
    
    @property
    @abstractmethod
    def template_name(self) -> str:
        """
        Return the template path relative to templates/.
        
        Examples:
            - "pages/windows_doors.html"
            - "pages/cover.html"
        """
        pass
    
    @abstractmethod
    def get_context(self, config: PageConfig, **kwargs) -> dict:
        """
        Build the template context dictionary.
        
        This method should call the appropriate renderers and generators
        to produce all the content needed by the template.
        
        Args:
            config: Page configuration with data
            **kwargs: Additional context (e.g., logos, page_number)
            
        Returns:
            Dictionary of template variables
        """
        pass
