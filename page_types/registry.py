"""Page registry."""

from __future__ import annotations

from typing import Type

from page_types.base import PageBase


class PageRegistry:
    """
    Registry for page types - enables plugin architecture.
    
    Usage:
        @PageRegistry.register("windows_doors")
        class WindowsDoorsPage(PageBase):
            ...
        
        # Later:
        page_class = PageRegistry.get("windows_doors")
        page = page_class()
    """
    
    _pages: dict[str, Type[PageBase]] = {}
    
    @classmethod
    def register(cls, page_type: str):
        """Decorator to register a page type."""
        def decorator(page_class: Type[PageBase]) -> Type[PageBase]:
            cls._pages[page_type] = page_class
            return page_class
        return decorator
    
    @classmethod
    def get(cls, page_type: str) -> Type[PageBase]:
        """Get page class by type name."""
        if page_type not in cls._pages:
            available = ", ".join(cls._pages.keys()) or "none"
            raise ValueError(
                f"Unknown page type: '{page_type}'. Available: {available}"
            )
        return cls._pages[page_type]
    
    @classmethod
    def list_types(cls) -> list[str]:
        """List all registered page types."""
        return list(cls._pages.keys())
    
    @classmethod
    def is_registered(cls, page_type: str) -> bool:
        """Check if a page type is registered."""
        return page_type in cls._pages
