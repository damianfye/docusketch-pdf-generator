"""SCSS compilation utilities."""

from pathlib import Path

import sass


def compile_scss(scss_path: Path | str) -> str:
    """
    Compile SCSS file to CSS string.
    
    Args:
        scss_path: Path to the main SCSS file
        
    Returns:
        Compiled CSS string
    """
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
    """
    Compile SCSS string to CSS.
    
    Args:
        scss_content: SCSS content as string
        include_paths: Optional list of paths for @import resolution
        
    Returns:
        Compiled CSS string
    """
    css = sass.compile(
        string=scss_content,
        include_paths=include_paths or [],
        output_style="compressed",
    )
    
    return css
