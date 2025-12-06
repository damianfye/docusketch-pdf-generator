"""Page types - plugin architecture for different page layouts."""

from page_types.base import PageBase
from page_types.registry import PageRegistry
from page_types.windows_doors import WindowsDoorsPage

__all__ = [
    "PageBase",
    "PageRegistry",
    "WindowsDoorsPage",
]
