"""
MarkdownPDFConverter - A convenience wrapper for converting PDFs to Markdown using PyMuPDF4LLM.

This module provides a simple interface for converting PDF files to Markdown format,
preserving text formatting, tables, and other structural elements.
"""

import logging
from pathlib import Path
from typing import Union

_log = logging.getLogger(__name__)


class MarkdownPDFConverter:
    """
    A simple converter class for converting PDF files to Markdown format using PyMuPDF4LLM.

    This class provides an easy-to-use interface for PDF to Markdown conversion,
    using the PyMuPDF4LLMBackend internally. It preserves:
    - Text formatting (bold, italic, headers)
    - Table structure and alignment
    - Images
    - Multi-column layouts
    - Code blocks

    Note: This class uses the PyMuPDF4LLMBackend internally when all dependencies
    are available. If Docling dependencies are missing, it falls back to using
    pymupdf4llm directly.

    Example:
        ```python
        from docling import MarkdownPDFConverter

        # Create a converter instance
        converter = MarkdownPDFConverter()

        # Convert a PDF to Markdown
        markdown_content = converter.pdf_to_markdown("path/to/sample.pdf")

        # Save to a file
        with open("output.md", "w") as f:
            f.write(markdown_content)
        ```
    """

    def __init__(self):
        """Initialize the MarkdownPDFConverter."""
        _log.debug("MarkdownPDFConverter initialized")

    def pdf_to_markdown(self, pdf_path: Union[str, Path]) -> str:
        """
        Convert a PDF file to Markdown format.

        Args:
            pdf_path: Path to the PDF file (string or Path object)

        Returns:
            str: The Markdown content as a string

        Raises:
            FileNotFoundError: If the PDF file does not exist
            RuntimeError: If the conversion fails
            ImportError: If pymupdf4llm is not installed

        Example:
            ```python
            converter = MarkdownPDFConverter()
            markdown = converter.pdf_to_markdown("document.pdf")
            print(markdown)
            ```
        """
        # Convert to Path object if string
        if isinstance(pdf_path, str):
            pdf_path = Path(pdf_path)

        # Check if file exists
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        _log.info(f"Converting PDF to Markdown: {pdf_path}")

        try:
            # Import the backend here to avoid heavy imports at module level
            from docling.backend.pymupdf4llm_backend import PyMuPDF4LLMBackend
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.document import InputDocument
        except ImportError:
            # If Docling dependencies are not available, fall back to direct pymupdf4llm usage
            _log.warning("Could not import Docling backend, using pymupdf4llm directly")
            try:
                import pymupdf4llm
            except ImportError as e2:
                raise ImportError(
                    "pymupdf4llm is required for PDF to Markdown conversion. "
                    "Install it with: pip install 'docling[pymupdf4llm]' or pip install pymupdf4llm"
                ) from e2

            try:
                markdown_content = pymupdf4llm.to_markdown(str(pdf_path))
                _log.info(f"Successfully converted PDF to Markdown ({len(markdown_content)} chars)")
                return markdown_content
            except Exception as e3:
                _log.error(f"Failed to convert PDF to Markdown: {e3}")
                raise RuntimeError(f"PDF to Markdown conversion failed: {e3}") from e3

        try:
            # Use the PyMuPDF4LLM backend to perform the conversion
            in_doc = InputDocument(
                path_or_stream=pdf_path,
                format=InputFormat.PDF,
                backend=PyMuPDF4LLMBackend,
                filename=pdf_path.name,
            )

            backend = PyMuPDF4LLMBackend(
                in_doc=in_doc,
                path_or_stream=pdf_path,
            )

            # Get the markdown content from the backend
            markdown_content = backend.markdown_content

            _log.info(f"Successfully converted PDF to Markdown ({len(markdown_content)} chars)")

            return markdown_content

        except Exception as e:
            _log.error(f"Failed to convert PDF to Markdown: {e}")
            raise RuntimeError(f"PDF to Markdown conversion failed: {e}") from e
