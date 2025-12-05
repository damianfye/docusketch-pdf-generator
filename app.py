"""
DocuSketch PDF Report Generator - Streamlit Application

Layer 4: User interface for editing table data, uploading assets,
and generating PDF reports.
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from models.primitives import Point, WallPolygon
from models.table import TableRow, TableData
from models.document import PageConfig, PageMetadata, DocumentConfig
from core.generator import DocumentGenerator


# === Configuration ===
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
DATA_DIR = PROJECT_ROOT / "data" / "samples"  # Sample data files
LOGOS_DIR = ASSETS_DIR / "logos"  # Static logo assets


# === Helper Functions ===

def load_default_table() -> pd.DataFrame:
    """Load default table data from CSV."""
    csv_path = DATA_DIR / "table_data.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path, index_col=0)
        # Remove the Total row for editing (we'll compute it)
        df = df[df["Wall"] != "Total"]
        return df
    
    # Fallback default
    return pd.DataFrame({
        "Wall": ["B1", "B2", "B3", ""],
        "Window/Door": ["W1", "W2", "W3", "W4"],
        "Area, ft²": [9.68, 49.32, 41.49, 5.81],
        "Perimeter, ft": [12.5, 31.72, 31.24, 9.66],
        "Size (WxH), ft": ["3.42 x 2.83", "11.61 x 4.25", "12.23 x 3.39", "2.26 x 2.57"],
    })


def load_walls() -> list[WallPolygon]:
    """Load wall data from JSON."""
    json_path = DATA_DIR / "wall_data.json"
    if not json_path.exists():
        return []
    
    with open(json_path) as f:
        data = json.load(f)
    
    walls = []
    for wall_coords in data.get("walls", []):
        points = [Point(x=coord[0], y=coord[1]) for coord in wall_coords]
        walls.append(WallPolygon(points=points))
    
    return walls


def load_default_svg() -> str:
    """Load default wall projection SVG."""
    svg_path = DATA_DIR / "top.svg"
    if svg_path.exists():
        return svg_path.read_text()
    return ""


def load_default_panorama() -> bytes:
    """Load default panorama image."""
    pano_path = DATA_DIR / "pano.jpg"
    if pano_path.exists():
        return pano_path.read_bytes()
    return b""


def load_logo_svg() -> str:
    """Load DocuSketch logo SVG."""
    logo_path = LOGOS_DIR / "new_logo.svg"
    if logo_path.exists():
        return logo_path.read_text()
    return ""


def load_logo_powered() -> bytes:
    """Load powered by logo PNG."""
    logo_path = LOGOS_DIR / "new_logo_powered.png"
    if logo_path.exists():
        return logo_path.read_bytes()
    return b""


def dataframe_to_table_data(df: pd.DataFrame) -> TableData:
    """Convert edited DataFrame to TableData model."""
    rows = []
    for _, row in df.iterrows():
        # Handle nan values from pandas
        wall = row.get("Wall")
        wall = str(wall) if pd.notna(wall) else ""
        
        window_door = row.get("Window/Door", "")
        window_door = str(window_door) if pd.notna(window_door) else ""
        
        size = row.get("Size (WxH), ft", "")
        size = str(size) if pd.notna(size) else ""
        
        rows.append(TableRow(
            wall=wall or None,
            window_door=window_door,
            area_sqft=float(row.get("Area, ft²", 0) or 0),
            perimeter_ft=float(row.get("Perimeter, ft", 0) or 0),
            size=size,
        ))
    
    return TableData.from_rows(rows)


def build_document_config(
    doc_id: str,
    address: str,
    section_name: str,
    table_df: pd.DataFrame,
    wall_projection_svg: str,
    panorama_bytes: bytes,
    walls: list[WallPolygon],
) -> DocumentConfig:
    """Build DocumentConfig from UI state."""
    return DocumentConfig(
        pages=[
            PageConfig(
                page_type="windows_doors",
                metadata=PageMetadata(
                    title="Windows and Doors",
                    document_id=doc_id,
                    address=address,
                    section_name=section_name,
                ),
                table_data=dataframe_to_table_data(table_df),
                walls=walls,
                wall_projection_svg=wall_projection_svg,
                panorama_image=panorama_bytes,
            )
        ],
        logo_svg=load_logo_svg(),
        logo_powered_png=load_logo_powered(),
    )


# === Streamlit App ===

st.set_page_config(
    page_title="DocuSketch PDF Generator",
    page_icon="📄",
    layout="wide",
)

st.title("DocuSketch PDF Report Generator")

# === Sidebar: Document Settings ===
with st.sidebar:
    st.header("📋 Document Settings")
    
    doc_id = st.text_input("Document ID", value="Test")
    address = st.text_input("Address", value="127 Example St, Sample City, CA 90210")
    section_name = st.text_input("Section Name", value="Back")
    
    st.divider()
    
    st.header("📁 Assets")
    
    # SVG upload
    uploaded_svg = st.file_uploader(
        "Wall Projection SVG",
        type=["svg"],
        help="Replace the wall projection (top.svg)",
    )
    
    # Panorama upload
    uploaded_pano = st.file_uploader(
        "Panorama Image",
        type=["jpg", "jpeg", "png"],
        help="Replace the 360° panorama image",
    )


# === Main Area ===

# Table Editor
st.header("📊 Table Data")
st.caption("Edit the measurements below. Changes will be reflected in the generated PDF.")

# Load or use session state
if "table_df" not in st.session_state:
    st.session_state.table_df = load_default_table()

edited_df = st.data_editor(
    st.session_state.table_df,
    column_config={
        "Wall": st.column_config.TextColumn("Wall", width="small"),
        "Window/Door": st.column_config.TextColumn("Window/Door", width="small"),
        "Area, ft²": st.column_config.NumberColumn("Area, ft²", format="%.2f"),
        "Perimeter, ft": st.column_config.NumberColumn("Perimeter, ft", format="%.2f"),
        "Size (WxH), ft": st.column_config.TextColumn("Size (WxH), ft"),
    },
    num_rows="dynamic",
    width="stretch",
    key="table_editor",
)

# Update session state
st.session_state.table_df = edited_df

st.divider()

# Actions
col1, col2 = st.columns(2)

with col1:
    generate_clicked = st.button(
        "🔄 Generate PDF",
        type="primary",
        width="stretch",
    )

with col2:
    if "pdf_bytes" in st.session_state:
        st.download_button(
            "📥 Download PDF",
            st.session_state.pdf_bytes,
            file_name="docusketch_report.pdf",
            mime="application/pdf",
            width="stretch",
        )
    else:
        st.button(
            "📥 Download PDF",
            disabled=True,
            width="stretch",
        )

# Generate PDF
if generate_clicked:
    with st.spinner("Generating PDF..."):
        try:
            # Get SVG content
            if uploaded_svg:
                wall_projection_svg = uploaded_svg.read().decode("utf-8")
            else:
                wall_projection_svg = load_default_svg()
            
            # Get panorama
            if uploaded_pano:
                panorama_bytes = uploaded_pano.read()
            else:
                panorama_bytes = load_default_panorama()
            
            # Load walls
            walls = load_walls()
            
            # Build config
            config = build_document_config(
                doc_id=doc_id,
                address=address,
                section_name=section_name,
                table_df=edited_df,
                wall_projection_svg=wall_projection_svg,
                panorama_bytes=panorama_bytes,
                walls=walls,
            )
            
            # Generate PDF
            generator = DocumentGenerator()
            pdf_bytes = generator.generate(config)
            
            # Store in session
            st.session_state.pdf_bytes = pdf_bytes
            
            st.success("✅ PDF generated successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error generating PDF: {e}")
            raise e


# Info
st.divider()
st.caption("DocuSketch PDF Report Generator - Interview Task")
