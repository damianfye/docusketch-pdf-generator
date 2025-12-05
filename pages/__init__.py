"""Page types - plugin architecture for different page layouts."""

from pages.base import PageBase
from pages.registry import PageRegistry
from pages.windows_doors import WindowsDoorsPage

__all__ = [
    "PageBase",
    "PageRegistry",
    "WindowsDoorsPage",
]
