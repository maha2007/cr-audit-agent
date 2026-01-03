"""
FCR Audit AI Agent Module
Handles Claude API integration and audit processing for Fundamental Credit Review.
"""

__version__ = "2.0.0"

from .claude_client import ClaudeClient
from .audit_prompt import AuditPrompt
from .result_processor import ResultProcessor
from .scoring import ScoringCalculator
from .extraction_integration import ExtractionIntegration

__all__ = [
    "ClaudeClient",
    "AuditPrompt",
    "ResultProcessor",
    "ScoringCalculator",
    "ExtractionIntegration",
]
