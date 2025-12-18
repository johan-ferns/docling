# PyMuPDF4LLM Backend Integration

This document explains how to use the PyMuPDF4LLM backend integration in Docling for converting PDF files to Markdown format.

## Installation

To use the PyMuPDF4LLM backend, install Docling with the `pymupdf4llm` optional dependency:

```bash
pip install docling[pymupdf4llm]
```

Or install `pymupdf4llm` separately:

```bash
pip install pymupdf4llm
```

## Usage

### Using MarkdownPDFConverter

The simplest way to convert PDFs to Markdown is using the `MarkdownPDFConverter` class.
This class uses the `PyMuPDF4LLMBackend` internally when all dependencies are available,
providing a simple API that returns Markdown strings:

```python
from docling import MarkdownPDFConverter

# Create a converter instance
converter = MarkdownPDFConverter()

# Convert a PDF to Markdown
markdown_content = converter.pdf_to_markdown("path/to/sample.pdf")

# Save the Markdown content to a file
with open("output.md", "w") as f:
    f.write(markdown_content)

print(f"Converted PDF to Markdown ({len(markdown_content)} characters)")
```

### Using the PyMuPDF4LLM Backend Directly

For advanced use cases where you need a `DoclingDocument` object or want to integrate
with Docling's document processing pipeline, you can use the PyMuPDF4LLM backend directly:

```python
from pathlib import Path
from docling.backend.pymupdf4llm_backend import PyMuPDF4LLMBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument

# Create an InputDocument
pdf_path = Path("path/to/sample.pdf")
in_doc = InputDocument(
    path_or_stream=pdf_path,
    format=InputFormat.PDF,
    backend=PyMuPDF4LLMBackend,
)

# Initialize the backend
backend = PyMuPDF4LLMBackend(
    in_doc=in_doc,
    path_or_stream=pdf_path,
)

# Get the Markdown content
markdown_content = backend.markdown_content

# Or convert to a DoclingDocument
doc = backend.convert()
```

### Using with DocumentConverter

To use PyMuPDF4LLM backend with `DocumentConverter`, you need to use `SimplePipeline`
(not `StandardPdfPipeline`) since PyMuPDF4LLM is a declarative backend:

```python
from pathlib import Path
from docling.document_converter import DocumentConverter, FormatOption
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.backend.pymupdf4llm_backend import PyMuPDF4LLMBackend
from docling.datamodel.base_models import InputFormat

# Option 1: Use FormatOption directly
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: FormatOption(
            pipeline_cls=SimplePipeline,
            backend=PyMuPDF4LLMBackend
        )
    }
)

# Option 2: If PyMuPDF4LLMFormatOption is available
try:
    from docling.document_converter import PyMuPDF4LLMFormatOption
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PyMuPDF4LLMFormatOption()
        }
    )
except ImportError:
    # PyMuPDF4LLMFormatOption not available, use Option 1
    pass

# Convert your PDF
result = converter.convert("path/to/sample.pdf")
doc = result.document

# Export to Markdown
markdown = doc.export_to_markdown()
```

**Important:** Do not use `PdfFormatOption` or `StandardPdfPipeline` with `PyMuPDF4LLMBackend`.
These are designed for paginated PDF backends like `DoclingParseV4DocumentBackend`.
Use `SimplePipeline` instead as shown above.

## Features

The PyMuPDF4LLM backend preserves:

- **Text formatting**: Bold, italic, headers, and other text styles
- **Tables**: Table structure and alignment
- **Images**: Embedded images and figures
- **Multi-column layouts**: Proper reading order for multi-column documents
- **Code blocks**: Code snippets and formulas
- **Lists**: Ordered and unordered lists

## Example

Here's a complete example that converts a PDF and saves it to Markdown:

```python
from docling import MarkdownPDFConverter
from pathlib import Path

def convert_pdf_to_markdown(pdf_path: str, output_path: str):
    """
    Convert a PDF file to Markdown format.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path where the Markdown file will be saved
    """
    # Create converter
    converter = MarkdownPDFConverter()
    
    # Convert PDF to Markdown
    print(f"Converting {pdf_path} to Markdown...")
    markdown = converter.pdf_to_markdown(pdf_path)
    
    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    print(f"✓ Saved Markdown to {output_path}")
    print(f"  ({len(markdown)} characters)")

if __name__ == "__main__":
    # Example usage
    convert_pdf_to_markdown(
        pdf_path="sample.pdf",
        output_path="sample.md"
    )
```

## Comparison with Standard Docling PDF Conversion

The PyMuPDF4LLM backend offers a different approach to PDF conversion:

- **PyMuPDF4LLM Backend**: Optimized for LLM consumption, focuses on clean Markdown output
- **Standard Docling Backend**: Provides richer document structure and metadata, better for complex document analysis

Choose the backend that best fits your use case:

- Use PyMuPDF4LLM for simple PDF to Markdown conversion with LLM-friendly output
- Use standard Docling backends for advanced document analysis, OCR, and rich metadata extraction

## Limitations

- Scanned PDFs may produce empty or poor-quality output (OCR is not built into this backend)
- Complex layouts may not be perfectly preserved
- Some formatting details may be lost in the conversion

## See Also

- [PyMuPDF4LLM Documentation](https://github.com/pymupdf/PyMuPDF4LLM)
- [Docling Documentation](https://docling-project.github.io/docling/)
