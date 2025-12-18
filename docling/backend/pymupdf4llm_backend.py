import logging
from io import BytesIO
from pathlib import Path
from typing import Set, Union

from docling_core.types.doc import DoclingDocument, DocumentOrigin

from docling.backend.abstract_backend import DeclarativeDocumentBackend
from docling.datamodel.backend_options import BaseBackendOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument

_log = logging.getLogger(__name__)


class PyMuPDF4LLMBackend(DeclarativeDocumentBackend):
    """
    Backend that uses PyMuPDF4LLM to convert PDFs to Markdown format.
    
    PyMuPDF4LLM provides optimized PDF to Markdown conversion with support for:
    - Text formatting (bold, italic, headers)
    - Tables with alignment
    - Images
    - Multi-column layouts
    - Code blocks
    """

    def __init__(
        self,
        in_doc: InputDocument,
        path_or_stream: Union[BytesIO, Path],
        options: BaseBackendOptions = BaseBackendOptions(),
    ):
        super().__init__(in_doc, path_or_stream, options)

        _log.debug("Starting PyMuPDF4LLMBackend...")

        self.valid = False
        self.markdown_content = ""

        try:
            # Import pymupdf4llm here to avoid import errors if not installed
            import pymupdf4llm
        except ImportError as e:
            raise ImportError(
                "pymupdf4llm is required for PyMuPDF4LLMBackend. "
                "Install it with: pip install 'docling[pymupdf4llm]' or pip install pymupdf4llm"
            ) from e

        try:
            # PyMuPDF4LLM can handle both file paths and file-like objects
            if isinstance(self.path_or_stream, BytesIO):
                # For BytesIO, we need to use pymupdf to open it first
                import pymupdf
                doc = pymupdf.open(stream=self.path_or_stream.getvalue(), filetype="pdf")
                self.markdown_content = pymupdf4llm.to_markdown(doc)
                doc.close()
            elif isinstance(self.path_or_stream, Path):
                # For file paths, pymupdf4llm can handle it directly
                self.markdown_content = pymupdf4llm.to_markdown(str(self.path_or_stream))
            else:
                raise ValueError(f"Unsupported input type: {type(self.path_or_stream)}")
            
            self.valid = True
            _log.debug(f"Successfully converted PDF to Markdown ({len(self.markdown_content)} chars)")
        except Exception as e:
            _log.error(f"Failed to initialize PyMuPDF4LLM backend: {e}")
            raise RuntimeError(
                f"Could not initialize PyMuPDF4LLM backend for file with hash {self.document_hash}."
            ) from e

    def is_valid(self) -> bool:
        return self.valid

    def unload(self):
        if isinstance(self.path_or_stream, BytesIO):
            self.path_or_stream.close()
        self.path_or_stream = None
        self.markdown_content = ""

    @classmethod
    def supports_pagination(cls) -> bool:
        return False

    @classmethod
    def supported_formats(cls) -> Set[InputFormat]:
        return {InputFormat.PDF}

    def convert(self) -> DoclingDocument:
        """
        Convert the PDF to a DoclingDocument by first converting to Markdown
        via PyMuPDF4LLM, then using the Markdown backend to parse it.
        """
        _log.debug("Converting PDF via PyMuPDF4LLM to Markdown...")

        if not self.is_valid():
            raise RuntimeError(
                f"Cannot convert PDF with {self.document_hash} because the backend failed to init."
            )

        # Import here to avoid circular dependency
        from docling.backend.md_backend import MarkdownDocumentBackend
        
        # Create a BytesIO stream from the markdown content
        md_stream = BytesIO(self.markdown_content.encode("utf-8"))
        
        # Create an InputDocument for the markdown
        md_in_doc = InputDocument(
            path_or_stream=md_stream,
            format=InputFormat.MD,
            backend=MarkdownDocumentBackend,
            filename=f"{self.file.stem}.md" if self.file else "converted.md",
        )
        
        # Use the MarkdownDocumentBackend to convert to DoclingDocument
        md_backend = MarkdownDocumentBackend(
            in_doc=md_in_doc,
            path_or_stream=md_stream,
        )
        
        doc = md_backend.convert()
        
        # Update the document origin to reflect that this came from a PDF
        doc.origin = DocumentOrigin(
            filename=self.file.name or "file.pdf",
            mimetype="application/pdf",
            binary_hash=self.document_hash,
        )
        
        return doc
