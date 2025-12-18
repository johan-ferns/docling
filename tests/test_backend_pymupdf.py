from pathlib import Path

import pytest
from docling_core.types.doc import BoundingBox

from docling.backend.pymupdf_backend import (
    PyMuPDFDocumentBackend,
    PyMuPDFPageBackend,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


@pytest.fixture
def test_doc_path():
    return Path("./tests/data/pdf/2206.01062.pdf")


def _get_backend(pdf_doc):
    in_doc = InputDocument(
        path_or_stream=pdf_doc,
        format=InputFormat.PDF,
        backend=PyMuPDFDocumentBackend,
    )

    doc_backend = in_doc._backend
    return doc_backend


def test_get_text_from_rect(test_doc_path):
    """Test extracting text from a specific rectangle on the page."""
    doc_backend = _get_backend(test_doc_path)
    page_backend: PyMuPDFPageBackend = doc_backend.load_page(0)

    # Get the title text of the DocLayNet paper
    textpiece = page_backend.get_text_in_rect(
        bbox=BoundingBox(l=102, t=77, r=511, b=124)
    )
    
    # The text should contain the title
    assert "DocLayNet" in textpiece or "Document-Layout" in textpiece


def test_crop_page_image(test_doc_path):
    """Test cropping a page image."""
    doc_backend = _get_backend(test_doc_path)
    page_backend: PyMuPDFPageBackend = doc_backend.load_page(0)

    # Crop out a region from the DocLayNet paper
    img = page_backend.get_page_image(
        scale=2, cropbox=BoundingBox(l=317, t=246, r=574, b=527)
    )
    
    # Verify image was created
    assert img is not None
    assert img.width > 0
    assert img.height > 0


def test_num_pages(test_doc_path):
    """Test getting the number of pages in the document."""
    doc_backend = _get_backend(test_doc_path)
    assert doc_backend.page_count() == 9


def test_text_cells(test_doc_path):
    """Test extracting text cells from a page."""
    doc_backend = _get_backend(test_doc_path)
    page_backend: PyMuPDFPageBackend = doc_backend.load_page(0)
    
    cells = list(page_backend.get_text_cells())
    
    # Should have extracted some text cells
    assert len(cells) > 0
    
    # Cells should have text
    assert any(cell.text.strip() for cell in cells)


def test_get_segmented_page(test_doc_path):
    """Test getting a segmented page."""
    doc_backend = _get_backend(test_doc_path)
    page_backend: PyMuPDFPageBackend = doc_backend.load_page(0)
    
    segmented_page = page_backend.get_segmented_page()
    
    assert segmented_page is not None
    assert segmented_page.has_textlines
    assert len(segmented_page.textline_cells) > 0


def test_get_page_size(test_doc_path):
    """Test getting page dimensions."""
    doc_backend = _get_backend(test_doc_path)
    page_backend: PyMuPDFPageBackend = doc_backend.load_page(0)
    
    size = page_backend.get_size()
    
    assert size.width > 0
    assert size.height > 0


def test_get_bitmap_rects(test_doc_path):
    """Test getting image bounding boxes from a page."""
    doc_backend = _get_backend(test_doc_path)
    
    # Try different pages to find one with images
    for page_no in range(min(3, doc_backend.page_count())):
        page_backend: PyMuPDFPageBackend = doc_backend.load_page(page_no)
        bitmap_rects = list(page_backend.get_bitmap_rects())
        
        # If we found images, verify they have valid bounding boxes
        if bitmap_rects:
            for rect in bitmap_rects:
                assert rect.area() > 0
            break


def test_document_conversion_with_pymupdf(test_doc_path):
    """Test full document conversion using PyMuPDF backend."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = False

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, backend=PyMuPDFDocumentBackend
            )
        }
    )
    
    conv_res = doc_converter.convert(test_doc_path)
    
    # Verify conversion succeeded
    assert conv_res.document is not None
    
    # Export to markdown and verify we got some content
    markdown = conv_res.document.export_to_markdown()
    assert len(markdown) > 0
    assert "DocLayNet" in markdown or "document" in markdown.lower()


def test_invalid_page(test_doc_path):
    """Test handling of invalid page numbers."""
    doc_backend = _get_backend(test_doc_path)
    
    # Try to load a page beyond the document
    page_backend = doc_backend.load_page(999)
    
    # Should be marked as invalid
    assert not page_backend.is_valid()
