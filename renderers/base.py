"""Base class for all renderers."""

from abc import ABC, abstractmethod


class RendererBase(ABC):
    """
    Abstract base for rendering tools.
    
    A renderer is a pure transformation:
        Input data → Embeddable output (HTML string, SVG string, data URI)
    
    Renderers have NO knowledge of pages or documents.
    They just transform data.
    """
    
    @abstractmethod
    def render(self) -> str:
        """
        Transform input data to output string.
        
        Returns:
            String ready for embedding in HTML template
        """
        pass
