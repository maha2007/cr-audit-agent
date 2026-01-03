"""
Claude 4.5 Sonnet PDF Extractor
Uses Claude's Visual API to convert PDFs to Markdown.
"""

import base64
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class ClaudeExtractor:
    """Extract PDF content using Claude 4.5 Sonnet Visual API."""
    
    SYSTEM_PROMPT = """You are an expert document digitizer. Your task is to convert the attached PDF into a high-fidelity Markdown document. 
- **Text:** Preserve all headings, lists, and prose exactly.
- **Tables:** Reconstruct every table into a clean Github-flavored Markdown table. DO NOT skip any rows or columns.
- **Images/Charts:** For every image or chart, provide a descriptive placeholder in brackets like `[Chart: Sales growth 2023-2025 showing 15% increase]` so the context is preserved.
- **Layout:** Maintain the logical reading order. If the document is multi-column, linearize it correctly.
- **Page Markers:** If possible, include page breaks or page number markers to help identify page boundaries."""
    
    MAX_PAGES_PER_REQUEST = 100
    
    def __init__(self, output_dir: str = "output", max_tokens: int = 4096):
        """
        Initialize Claude extractor.
        
        Args:
            output_dir: Output directory for saving Markdown files
            max_tokens: Maximum tokens for Claude response (default: 4096)
        """
        # Try Streamlit secrets first (for deployment on Streamlit Cloud)
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
                self.api_key = st.secrets['ANTHROPIC_API_KEY']
            else:
                # Fall back to environment variable (for local development)
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
        except (ImportError, AttributeError):
            # Streamlit not available, use environment variable
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "For local development: Set it in .env file. "
                "For Streamlit Cloud: Set it in Streamlit Secrets (Settings → Secrets)."
            )
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_tokens = max_tokens
        
        # Initialize Anthropic client
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic>=0.40.0")
    
    def _get_pdf_page_count(self, pdf_path: str) -> int:
        """
        Get page count of PDF (for splitting large PDFs).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Number of pages
        """
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                return len(pdf_reader.pages)
        except Exception:
            # Fallback: assume single page or use a default
            return 1
    
    def _read_pdf_as_base64(self, pdf_path: str) -> bytes:
        """
        Read PDF file and encode as base64.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Base64-encoded PDF bytes
        """
        with open(pdf_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _split_pdf_if_needed(self, pdf_path: str) -> list:
        """
        Split PDF into batches if it exceeds page limit.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of PDF paths (original if no split needed, or split files)
        """
        page_count = self._get_pdf_page_count(pdf_path)
        
        if page_count <= self.MAX_PAGES_PER_REQUEST:
            return [pdf_path]
        
        # For now, return original - splitting PDFs is complex
        # In production, you might want to use a PDF splitting library
        # For this implementation, we'll process the full PDF and let Claude handle it
        # (Claude may handle large PDFs, but if it fails, we'll get an error)
        return [pdf_path]
    
    def extract(self, pdf_path: str, max_retries: int = 3) -> str:
        """
        Extract PDF content to Markdown using Claude.
        
        Args:
            pdf_path: Path to PDF file
            max_retries: Maximum number of retry attempts
            
        Returns:
            Markdown string
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Read PDF as base64
        pdf_base64 = self._read_pdf_as_base64(str(pdf_path))
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Call Claude API with PDF document
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=self.max_tokens,
                    system=self.SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "document",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "application/pdf",
                                        "data": pdf_base64
                                    }
                                }
                            ]
                        }
                    ],
                    extra_headers={
                        "anthropic-beta": "pdfs-2024-09-25"
                    }
                )
                
                # Extract Markdown from response
                if response.content and len(response.content) > 0:
                    markdown_text = ""
                    for block in response.content:
                        if hasattr(block, 'text'):
                            markdown_text += block.text
                        elif isinstance(block, str):
                            markdown_text += block
                    
                    # Save Markdown to file
                    markdown_path = self.output_dir / f"{pdf_path.stem}.md"
                    with open(markdown_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_text)
                    
                    return markdown_text
                else:
                    raise ValueError("Empty response from Claude API")
                    
            except Exception as e:
                error_str = str(e).lower()
                
                # Check for overloaded error
                if "overloaded" in error_str or "rate_limit" in error_str:
                    last_error = e
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError(
                            f"Claude API overloaded after {max_retries} attempts: {str(e)}"
                        ) from e
                else:
                    # Don't retry on other errors
                    raise RuntimeError(f"Claude API request failed: {str(e)}") from e
        
        # Should not reach here
        raise RuntimeError(f"Claude API request failed: {str(last_error)}") from last_error

