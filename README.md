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

# Run tests
pytest
```

## Architecture

The project follows a layered architecture with clear separation of concerns:

```
LAYER 4: app.py              → Streamlit UI
LAYER 3: core/               → Document assembly & PDF generation
LAYER 2: pages/              → Page type plugins (extensible)
LAYER 1: renderers/ + generators/ → Data transformation
LAYER 0: models/ + utils/    → Data models & pure utilities
```

**Key principle**: Each layer only imports from layers below, never up.

## Project Structure

```
docusketch-pdf-generator/
├── app.py                  # Streamlit entry point
├── core/                   # Document generation engine
│   ├── generator.py        # Main orchestrator
│   ├── pdf_renderer.py     # WeasyPrint wrapper
│   └── template_engine.py  # Jinja2 + SCSS
├── pages/                  # Page type plugins
│   ├── base.py             # Abstract page interface
│   ├── registry.py         # Plugin registration
│   └── windows_doors.py    # Windows & Doors page
├── renderers/              # Embed existing data
├── generators/             # Create new content
│   └── floor_plan.py       # Boundary wall algorithm
├── models/                 # Pydantic data models
├── utils/                  # Pure utility functions
├── templates/              # Jinja2 HTML templates
├── styles/                 # SCSS stylesheets
├── data/samples/           # Sample data files
├── assets/logos/           # Static logo assets
└── tests/                  # Unit tests
```

## Technologies

| Component       | Technology     |
| --------------- | -------------- |
| UI Framework    | Streamlit      |
| PDF Generation  | WeasyPrint     |
| Templating      | Jinja2         |
| Styling         | SCSS (libsass) |
| Data Validation | Pydantic       |
| Geometry        | NumPy, SciPy   |

## The Boundary Wall Algorithm

The floor plan generator identifies which walls form the exterior boundary of the building. These are rendered in blue to distinguish them from interior walls.

See `generators/floor_plan.py` and `utils/geometry.py` for implementation details.
