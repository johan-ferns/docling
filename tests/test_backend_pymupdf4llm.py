from pathlib import Path

import pytest

from docling.markdown_pdf_converter import MarkdownPDFConverter


def test_markdown_pdf_converter_basic():
    """Test basic MarkdownPDFConverter functionality."""
    # Use a PDF from the test data
    pdf_path = Path("tests/data/pdf/2206.01062.pdf")
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    # Create converter
    converter = MarkdownPDFConverter()
    
    # Convert PDF to Markdown
    markdown = converter.pdf_to_markdown(pdf_path)
    
    # Check that markdown was generated
    assert isinstance(markdown, str)
    assert len(markdown) > 0
    # Check for expected content
    assert "DocLayNet" in markdown or "document" in markdown.lower()


def test_markdown_pdf_converter_file_not_found():
    """Test that MarkdownPDFConverter raises FileNotFoundError for missing files."""
    converter = MarkdownPDFConverter()
    
    with pytest.raises(FileNotFoundError):
        converter.pdf_to_markdown("nonexistent_file.pdf")


def test_markdown_pdf_converter_string_path():
    """Test that MarkdownPDFConverter accepts string paths."""
    pdf_path = "tests/data/pdf/2206.01062.pdf"
    
    if not Path(pdf_path).exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    converter = MarkdownPDFConverter()
    markdown = converter.pdf_to_markdown(pdf_path)
    
    assert isinstance(markdown, str)
    assert len(markdown) > 0


def test_markdown_pdf_converter_multiple_conversions():
    """Test that converter can be reused for multiple conversions."""
    pdf_path = Path("tests/data/pdf/2206.01062.pdf")
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF not found: {pdf_path}")
    
    converter = MarkdownPDFConverter()
    
    # First conversion
    markdown1 = converter.pdf_to_markdown(pdf_path)
    assert isinstance(markdown1, str)
    assert len(markdown1) > 0
    
    # The converter should be stateless, so we can just verify it works again
    # without comparing results (pymupdf4llm might have nondeterministic output)
    pdf_path2 = Path("tests/data/pdf/code_and_formula.pdf")
    if pdf_path2.exists():
        markdown2 = converter.pdf_to_markdown(pdf_path2)
        assert isinstance(markdown2, str)

