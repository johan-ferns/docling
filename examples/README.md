# Docling Examples

This directory contains example scripts demonstrating various features of Docling.

## PyMuPDF4LLM Integration

### `pymupdf4llm_example.py`

A simple example showing how to convert PDF files to Markdown using the `MarkdownPDFConverter` class.

**Usage:**

1. Install Docling with the pymupdf4llm optional dependency:
   ```bash
   pip install docling[pymupdf4llm]
   ```

2. Place a PDF file named `sample.pdf` in the current directory

3. Run the example:
   ```bash
   python examples/pymupdf4llm_example.py
   ```

The script will convert `sample.pdf` to `sample.md` and display a preview of the conversion.

**Features demonstrated:**
- Creating a `MarkdownPDFConverter` instance
- Converting a PDF to Markdown
- Saving the Markdown output to a file
- Error handling for missing files

For more information, see the [PyMuPDF4LLM Integration Documentation](../docs/pymupdf4llm_integration.md).
