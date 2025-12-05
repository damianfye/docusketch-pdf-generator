"""Encoding utilities for embedding assets in HTML."""

import base64


def to_data_uri(data: bytes, mime_type: str) -> str:
    """
    Convert bytes to a data URI for embedding in HTML.
    
    Args:
        data: Raw bytes to encode
        mime_type: MIME type (e.g., "image/jpeg", "image/png")
        
    Returns:
        Data URI string ready for src attribute
    """
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def svg_to_data_uri(svg_string: str) -> str:
    """
    Convert SVG string to a data URI.
    
    Args:
        svg_string: SVG content as string
        
    Returns:
        Data URI string
    """
    return to_data_uri(svg_string.encode("utf-8"), "image/svg+xml")


def image_to_data_uri(image_bytes: bytes, filename: str = "") -> str:
    """
    Convert image bytes to data URI, inferring MIME type from filename.
    
    Args:
        image_bytes: Raw image bytes
        filename: Optional filename to infer MIME type
        
    Returns:
        Data URI string
    """
    # Infer MIME type from extension or default to jpeg
    mime_type = "image/jpeg"
    if filename.lower().endswith(".png"):
        mime_type = "image/png"
    elif filename.lower().endswith(".svg"):
        mime_type = "image/svg+xml"
    elif filename.lower().endswith(".gif"):
        mime_type = "image/gif"
    
    return to_data_uri(image_bytes, mime_type)
