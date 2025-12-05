"""
Application constants and configuration values.

Centralizes magic numbers and configuration to avoid scattering them across the codebase.
"""

from pathlib import Path

# === Paths ===
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data" / "samples"
ASSETS_DIR = PROJECT_ROOT / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STYLES_DIR = PROJECT_ROOT / "styles"
OUTPUT_DIR = PROJECT_ROOT / "output"

# === PDF Generation ===
PDF_PAGE_WIDTH_MM = 210  # A4
PDF_PAGE_HEIGHT_MM = 297
PDF_MARGIN_MM = 15

# === Floor Plan Rendering ===
FLOOR_PLAN_WIDTH = 200
FLOOR_PLAN_HEIGHT = 200
FLOOR_PLAN_PADDING = 10.0

# === Colors (DocuSketch brand) ===
COLOR_PRIMARY = "#1A637E"
COLOR_BOUNDARY_WALL = "#5AA0D6"  # Blue for highlighted walls
COLOR_WALL_FILL = "#E6F1F9"      # Light fill for other walls
COLOR_WALL_STROKE = "#000000"    # Black outline
STROKE_WIDTH = 2.0

# === Section Names ===
SECTION_BACK = "back"
SECTION_FRONT = "front"
SECTION_LEFT = "left"
SECTION_RIGHT = "right"
VALID_SECTIONS = {SECTION_BACK, SECTION_FRONT, SECTION_LEFT, SECTION_RIGHT}
