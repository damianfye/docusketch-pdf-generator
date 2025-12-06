# DocuSketch PDF Report Generator

A Streamlit application for generating PDF reports from floor plan data.

## Features

- **Editable Table**: Modify window/door measurements directly in the UI
- **Asset Replacement**: Upload custom SVG projections and panorama images
- **PDF Generation**: Generate professional PDF reports using WeasyPrint
- **Boundary Wall Detection**: Algorithmically identifies exterior walls for the floor plan

## Quick Start

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix

# Install dependencies
pip install -e .

# Run the app
streamlit run app.py
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Run linter
ruff check .

# Run type checker
mypy .
```

## Architecture

The project follows a layered architecture with clear separation of concerns:

```
LAYER 4: app.py                   → Streamlit UI
LAYER 3: core/                    → Document assembly & PDF generation
LAYER 2: page_types/              → Page type plugins (extensible)
LAYER 1: renderers/ + generators/ → Data transformation
LAYER 0: models/ + utils/         → Data models & pure utilities
```

**Key principle**: Each layer only imports from layers below, never up.

## The Algorithm

The floor plan generator uses normal vectors and dot products to identify which walls are visible from a given viewing direction. Visible walls are highlighted in blue. See `docs/ALGORITHM_SOLUTION.md` for detailed explanation and `generators/visibility.py` for implementation.
