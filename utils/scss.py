"""SCSS compilation utilities."""

from __future__ import annotations

from pathlib import Path

import sass


def compile_scss(scss_path: Path | str) -> str:
    """Compile SCSS file to CSS string."""
    scss_path = Path(scss_path)
    
    if not scss_path.exists():
        raise FileNotFoundError(f"SCSS file not found: {scss_path}")
    
    # Compile with the directory as include path for @import
    css = sass.compile(
        filename=str(scss_path),
        include_paths=[str(scss_path.parent)],
        output_style="compressed",
    )
    
    return css


def compile_scss_string(scss_content: str, include_paths: list[str] | None = None) -> str:
    """Compile SCSS string to CSS."""
    css = sass.compile(
        string=scss_content,
        include_paths=include_paths or [],
        output_style="compressed",
    )
    
    return css
