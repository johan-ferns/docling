#!/usr/bin/env python3
"""
Example script demonstrating how to use the MarkdownPDFConverter
to convert PDF files to Markdown format.
"""

from pathlib import Path

from docling import MarkdownPDFConverter


def main():
    """Main function to demonstrate PDF to Markdown conversion."""

    # Create a converter instance
    converter = MarkdownPDFConverter()

    # Example 1: Convert a PDF file
    pdf_path = Path("sample.pdf")

    # Check if the example PDF exists
    if not pdf_path.exists():
        print(f"Example PDF not found: {pdf_path}")
        print("Please provide a PDF file named 'sample.pdf' in the current directory.")
        return

    print(f"Converting {pdf_path} to Markdown...")

    try:
        # Convert PDF to Markdown
        markdown_content = converter.pdf_to_markdown(pdf_path)

        # Save to output file
        output_path = pdf_path.with_suffix(".md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print("✓ Successfully converted PDF to Markdown!")
        print(f"  Output file: {output_path}")
        print(f"  Size: {len(markdown_content)} characters")

        # Show a preview
        print("\nPreview (first 300 characters):")
        print("-" * 80)
        print(markdown_content[:300])
        if len(markdown_content) > 300:
            print("...")
        print("-" * 80)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error during conversion: {e}")


if __name__ == "__main__":
    main()
