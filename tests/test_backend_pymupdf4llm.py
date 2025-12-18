from pathlib import Path

import pytest

from docling.backend.pymupdf4llm_backend import PyMuPDF4LLMBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument
from docling.markdown_pdf_converter import MarkdownPDFConverter


def test_pymupdf4llm_backend_basic():
    """Test basic PyMuPDF4LLM backend functionality."""
    # Use a PDF from the test data
    pdf_path = Path("tests/data_scanned/ocr_test.pdf")
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    # Create an InputDocument
    in_doc = InputDocument(
        path_or_stream=pdf_path,
        format=InputFormat.PDF,
        backend=PyMuPDF4LLMBackend,
    )
    
    # Initialize backend
    backend = PyMuPDF4LLMBackend(
        in_doc=in_doc,
        path_or_stream=pdf_path,
    )
    
    # Check that backend is valid
    assert backend.is_valid()
    
    # Check that markdown content was generated
    assert len(backend.markdown_content) > 0
    
    # Convert to DoclingDocument
    doc = backend.convert()
    
    # Verify document has content
    assert doc is not None
    assert doc.name is not None


def test_pymupdf4llm_backend_supported_formats():
    """Test that PyMuPDF4LLM backend supports PDF format."""
    assert InputFormat.PDF in PyMuPDF4LLMBackend.supported_formats()


def test_pymupdf4llm_backend_pagination():
    """Test that PyMuPDF4LLM backend does not support pagination."""
    assert not PyMuPDF4LLMBackend.supports_pagination()


def test_markdown_pdf_converter_basic():
    """Test basic MarkdownPDFConverter functionality."""
    # Use a PDF from the test data
    pdf_path = Path("tests/data_scanned/ocr_test.pdf")
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    # Create converter
    converter = MarkdownPDFConverter()
    
    # Convert PDF to Markdown
    markdown = converter.pdf_to_markdown(pdf_path)
    
    # Check that markdown was generated
    assert isinstance(markdown, str)
    assert len(markdown) > 0


def test_markdown_pdf_converter_file_not_found():
    """Test that MarkdownPDFConverter raises FileNotFoundError for missing files."""
    converter = MarkdownPDFConverter()
    
    with pytest.raises(FileNotFoundError):
        converter.pdf_to_markdown("nonexistent_file.pdf")


def test_markdown_pdf_converter_string_path():
    """Test that MarkdownPDFConverter accepts string paths."""
    pdf_path = "tests/data_scanned/ocr_test.pdf"
    
    if not Path(pdf_path).exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    converter = MarkdownPDFConverter()
    markdown = converter.pdf_to_markdown(pdf_path)
    
    assert isinstance(markdown, str)
    assert len(markdown) > 0
