"""
Data schematizer for extracting key-value pairs from text using regex and NER.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import Config


class DataSchematizer:
    """Extract key-value pairs from text using configurable patterns and NER."""
    
    def __init__(self, config_path: Optional[str] = None, output_dir: str = "output"):
        """
        Initialize data schematizer.
        
        Args:
            config_path: Path to patterns.json config file
            output_dir: Base output directory path (for logging)
        """
        self.config = Config(config_path)
        self.patterns = self.config.get_patterns()
        self.ner_labels = self.config.get_ner_labels()
        self.output_dir = Path(output_dir)
        self.logger = self._setup_logger()
        self.nlp = self._load_spacy_model()
    
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
    
    def _load_spacy_model(self):
        """Load spaCy NER model."""
        try:
            import spacy
            # Try to load the model
            try:
                nlp = spacy.load("en_core_web_sm")
                self.logger.info("Loaded spaCy model: en_core_web_sm")
                return nlp
            except OSError:
                self.logger.warning(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install it with: python -m spacy download en_core_web_sm"
                )
                return None
        except ImportError:
            self.logger.warning("spaCy not available, NER extraction will be skipped")
            return None
    
    def _extract_with_regex(self, text: str) -> Dict[str, str]:
        """
        Extract key-value pairs using regex patterns.
        
        Args:
            text: Text to extract from
            
        Returns:
            Dictionary of key-value pairs
        """
        key_value_pairs = {}
        
        for key, patterns in self.patterns.items():
            for pattern in patterns:
                try:
                    # Case-insensitive search
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        # Extract the captured group
                        value = match.group(1) if match.groups() else match.group(0)
                        # Only add if we don't already have a value for this key
                        # or if the new value is more specific (longer)
                        if key not in key_value_pairs or len(value) > len(key_value_pairs[key]):
                            key_value_pairs[key] = value.strip()
                            break  # Use first match for this key
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern for {key}: {pattern} - {e}")
                    continue
        
        return key_value_pairs
    
    def _extract_with_ner(self, text: str) -> Dict[str, str]:
        """
        Extract entities using spaCy NER.
        
        Args:
            text: Text to extract from
            
        Returns:
            Dictionary of entity types and values
        """
        if self.nlp is None:
            return {}
        
        key_value_pairs = {}
        
        try:
            # Process text with spaCy (limit to reasonable length to avoid memory issues)
            max_length = 1000000  # spaCy's default max length
            if len(text) > max_length:
                text = text[:max_length]
                self.logger.warning(f"Text truncated to {max_length} characters for NER processing")
            
            doc = self.nlp(text)
            
            # Extract entities matching our configured labels
            for ent in doc.ents:
                if ent.label_ in self.ner_labels:
                    # For entities that might appear multiple times, keep the longest/most specific
                    label = ent.label_
                    value = ent.text.strip()
                    
                    if label not in key_value_pairs or len(value) > len(key_value_pairs[label]):
                        key_value_pairs[label] = value
            
        except Exception as e:
            self.logger.error(f"Error during NER extraction: {e}")
        
        return key_value_pairs
    
    def extract(self, text: str) -> Dict[str, str]:
        """
        Extract key-value pairs from text using both regex and NER.
        
        Args:
            text: Text to extract from
            
        Returns:
            Combined dictionary of key-value pairs
        """
        if not text or not text.strip():
            return {}
        
        # Extract using regex patterns
        regex_pairs = self._extract_with_regex(text)
        
        # Extract using NER
        ner_pairs = self._extract_with_ner(text)
        
        # Combine results (regex takes precedence for overlapping keys)
        combined_pairs = {**ner_pairs, **regex_pairs}
        
        return combined_pairs
    
    def extract_from_pages(self, text_data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """
        Extract key-value pairs from page-by-page text data.
        
        Args:
            text_data: Dictionary mapping page keys to text content lists
            
        Returns:
            Dictionary mapping page keys to key-value pairs
        """
        schematized_data = {}
        
        for page_key, page_content in text_data.items():
            # Combine all text from the page
            page_text = " ".join([
                item.get("text", "") 
                for item in page_content 
                if isinstance(item, dict) and "text" in item
            ])
            
            # Extract key-value pairs
            key_value_pairs = self.extract(page_text)
            schematized_data[page_key] = key_value_pairs
        
        return schematized_data

