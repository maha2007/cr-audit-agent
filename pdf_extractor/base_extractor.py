"""
Base extractor class providing common functionality for all extractors.
"""

import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseExtractor(ABC):
    """Base class for all PDF extractors."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the base extractor.
        
        Args:
            output_dir: Base output directory path
        """
        self.output_dir = Path(output_dir)
        self.logger = self._setup_logger()
        self._ensure_output_dir()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        log_file = self.output_dir / "extraction.log"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not logger.handlers:
            # File handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _check_ocr_required(self, text: str, page_num: int) -> bool:
        """
        Check if a page requires OCR (scanned page).
        
        Args:
            text: Extracted text from the page
            page_num: Page number (1-indexed)
            
        Returns:
            True if OCR is required, False otherwise
        """
        if not text or not text.strip():
            self.logger.warning(f"Page {page_num}: OCR Required - No selectable text found")
            return True
        return False
    
    def _validate_pdf_path(self, pdf_path: str) -> bool:
        """
        Validate that the PDF file exists and is readable.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return False
        
        if not pdf_path.lower().endswith('.pdf'):
            self.logger.warning(f"File does not have .pdf extension: {pdf_path}")
        
        return True
    
    @abstractmethod
    def extract(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract data from PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted data
        """
        pass

