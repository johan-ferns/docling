# Docling - Document Conversion Library
# Import main components for convenience

def __getattr__(name):
    """Lazy import to avoid circular dependencies"""
    if name == "MarkdownPDFConverter":
        from docling.markdown_pdf_converter import MarkdownPDFConverter
        return MarkdownPDFConverter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["MarkdownPDFConverter"]
