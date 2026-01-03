"""
Configuration management for the PDF extractor.
"""

import json
import os
from pathlib import Path
from typing import Dict, List


class Config:
    """Configuration manager for patterns and settings."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to patterns.json file. If None, uses default.
        """
        if config_path is None:
            # Default to config/patterns.json relative to project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "patterns.json"
        
        self.config_path = Path(config_path)
        self.patterns: Dict[str, List[str]] = {}
        self.ner_labels: List[str] = []
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            self.patterns = config_data.get("patterns", {})
            self.ner_labels = config_data.get("ner_labels", [])
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")
    
    def get_patterns(self) -> Dict[str, List[str]]:
        """Get all regex patterns."""
        return self.patterns
    
    def get_ner_labels(self) -> List[str]:
        """Get NER labels to extract."""
        return self.ner_labels

