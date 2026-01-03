"""
Claude API Client for FCR Audit Analysis
"""

import os
import json
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    """Client for interacting with Anthropic Claude API."""
    
    def __init__(self, model: str = "claude-sonnet-4-5-20250929", thinking_level: str = "high", temperature: float = 1.0):
        """
        Initialize Claude client.
        
        Args:
            model: Model name (default: 'claude-sonnet-4-5-20250929', kept for compatibility)
            thinking_level: Thinking level ('high', 'medium', 'low') - kept for compatibility, not used by Claude
            temperature: Temperature setting (default: 1.0)
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
        
        # Always use Claude Sonnet 4.5
        self.model = "claude-sonnet-4-5-20250929"
        self.thinking_level = thinking_level  # Kept for compatibility
        self.temperature = temperature
        
        # Initialize the client
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic>=0.40.0")
    
    def send_audit_request(self, prompt: str, extraction_data: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """
        Send audit request to Claude API with retry logic.
        
        Args:
            prompt: The FCR audit prompt
            extraction_data: Structured extraction data from PDFs
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary containing the API response
            
        Raises:
            RuntimeError: If API request fails after all retries
            ValueError: If response cannot be parsed
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Format the full prompt with extraction data
                full_prompt = self._format_prompt(prompt, extraction_data)
                
                # Add JSON format instruction to system prompt with conciseness requirement
                system_prompt = """You are an FCR Audit AI Agent. You must respond with valid JSON only, no additional text or markdown formatting.

CRITICAL: Keep your justifications concise and focused. While you must cite specific Credit Policy Manual articles and provide detailed analysis, avoid excessive verbosity. Aim for clear, precise justifications that cover key points without unnecessary elaboration. This ensures the complete response fits within token limits."""
                
                # Call Claude API
                # Use higher max_tokens for complex audit responses with Credit Policy Manual references
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=16384,  # Increased to 16384 to handle detailed audit responses with manual citations
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ]
                )
                
                # #region agent log
                try:
                    with open("/Users/mahanawaz/FCR agent/.cursor/debug.log", "a") as f:
                        import json as json_module
                        f.write(json_module.dumps({
                            "sessionId": "debug-session",
                            "runId": "claude-response-check",
                            "hypothesisId": "A",
                            "location": "claude_client.py:api_response",
                            "message": "Claude API response metadata",
                            "data": {
                                "stop_reason": getattr(response, 'stop_reason', None),
                                "stop_sequence": getattr(response, 'stop_sequence', None),
                                "model": self.model,
                                "max_tokens": 16384,
                                "content_blocks": len(response.content) if response.content else 0,
                                "usage_input_tokens": getattr(response, 'usage', {}).get('input_tokens', None) if hasattr(response, 'usage') else None,
                                "usage_output_tokens": getattr(response, 'usage', {}).get('output_tokens', None) if hasattr(response, 'usage') else None
                            },
                            "timestamp": int(time.time() * 1000)
                        }) + "\n")
                except:
                    pass
                # #endregion
                
                # Parse JSON response
                if response.content and len(response.content) > 0:
                    text = ""
                    for block in response.content:
                        if hasattr(block, 'text'):
                            text += block.text
                        elif isinstance(block, str):
                            text += block
                    
                    # Try to parse JSON
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError as e:
                        # Try to extract JSON from text if wrapped
                        # Look for JSON block
                        if "```json" in text:
                            json_start = text.find("```json") + 7
                            json_end = text.find("```", json_start)
                            text = text[json_start:json_end].strip()
                        elif "```" in text:
                            json_start = text.find("```") + 3
                            json_end = text.find("```", json_start)
                            if json_end > json_start:
                                text = text[json_start:json_end].strip()
                        
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError as parse_err:
                            # #region agent log
                            try:
                                with open("/Users/mahanawaz/FCR agent/.cursor/debug.log", "a") as f:
                                    import json as json_module
                                    f.write(json_module.dumps({
                                        "sessionId": "debug-session",
                                        "runId": "claude-parse-error",
                                        "hypothesisId": "B",
                                        "location": "claude_client.py:json_parse_error",
                                        "message": "JSON parse error with response details",
                                        "data": {
                                            "error": str(parse_err),
                                            "text_length": len(text),
                                            "stop_reason": getattr(response, 'stop_reason', None),
                                            "text_preview": text[:500],
                                            "text_end": text[-500:] if len(text) > 500 else text,
                                            "usage_output_tokens": getattr(response, 'usage', {}).get('output_tokens', None) if hasattr(response, 'usage') else None
                                        },
                                        "timestamp": int(time.time() * 1000)
                                    }) + "\n")
                            except:
                                pass
                            # #endregion
                            
                            # If still failing, check if it's a truncation issue
                            if hasattr(response, 'stop_reason') and response.stop_reason == 'max_tokens':
                                raise ValueError(f"Response was truncated (max_tokens reached at 16384). The audit response with Credit Policy Manual citations is too long. Consider requesting more concise responses. Partial response: {text[:1000]}")
                            
                            # Try to find where JSON might be incomplete
                            # Look for the last complete closing brace/bracket
                            last_brace = text.rfind('}')
                            last_bracket = text.rfind(']')
                            last_complete = max(last_brace, last_bracket)
                            
                            if last_complete > 0 and last_complete < len(text) - 10:
                                # Try to extract up to the last complete structure
                                try:
                                    partial_text = text[:last_complete + 1]
                                    # Try to find the opening brace to see if we have a complete object
                                    first_brace = partial_text.find('{')
                                    if first_brace >= 0:
                                        return json.loads(partial_text[first_brace:])
                                except:
                                    pass
                            
                            raise ValueError(f"Failed to parse JSON response: {parse_err}. Response text length: {len(text)}, preview: {text[:1000]}, end: {text[-200:]}")
                else:
                    raise ValueError("No content in response")
                    
            except ValueError as e:
                # Don't retry on parsing errors
                raise ValueError(f"Failed to parse Claude response: {str(e)}") from e
            except Exception as e:
                error_str = str(e).lower()
                
                # Check for rate limit or overloaded errors
                if "rate_limit" in error_str or "overloaded" in error_str or "429" in error_str:
                    last_error = e
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError(
                            f"Claude API rate limited after {max_retries} attempts: {str(e)}"
                        ) from e
                else:
                    # Don't retry on other errors
                    raise RuntimeError(f"Claude API request failed: {str(e)}") from e
        
        # Should not reach here, but just in case
        raise RuntimeError(f"Claude API request failed: {str(last_error)}") from last_error
    
    def _format_prompt(self, prompt: str, extraction_data: Dict[str, Any]) -> str:
        """
        Format the full prompt with extraction data.
        
        Args:
            prompt: Base audit prompt
            extraction_data: Structured extraction data
            
        Returns:
            Formatted prompt string
        """
        # Format extraction data as readable text
        data_section = self._format_extraction_data(extraction_data)
        
        full_prompt = f"""{prompt}

# Input Data

## Extracted Document Content

{data_section}

Please analyze the above extracted content and provide your audit assessment in the specified JSON format.
"""
        return full_prompt
    
    def _format_extraction_data(self, extraction_data: Dict[str, Any]) -> str:
        """
        Format extraction data into readable text for Claude.
        
        Args:
            extraction_data: Structured extraction data
            
        Returns:
            Formatted text string
        """
        formatted = []
        
        # Handle both old format (pages dict) and new format (pages dict with nested structure)
        pages = extraction_data.get("pages", {})
        if not pages and isinstance(extraction_data, dict):
            # Try direct access if pages key doesn't exist
            pages = extraction_data
        
        for page_key, page_data in pages.items():
            formatted.append(f"\n## {page_key}\n")
            
            # Text content
            if "Text Content" in page_data:
                formatted.append("### Text Content:\n")
                for text_item in page_data["Text Content"]:
                    if isinstance(text_item, dict):
                        text_type = text_item.get("type", "body")
                        text = text_item.get("text", "")
                        if text:
                            formatted.append(f"[{text_type.upper()}] {text}\n")
            
            # Tables
            if "Table References" in page_data and page_data["Table References"]:
                formatted.append("### Tables:\n")
                for table_ref in page_data["Table References"]:
                    if isinstance(table_ref, dict):
                        table_id = table_ref.get("table_id", "Unknown")
                        # Include table data if available
                        if "data" in table_ref:
                            formatted.append(f"\n**Table: {table_id}**\n")
                            # Format table data
                            for row in table_ref["data"][:10]:  # Limit to first 10 rows
                                row_str = " | ".join([str(v) for v in row.values()])
                                formatted.append(f"{row_str}\n")
            
            # Key-value pairs
            if "KeyValuePairs" in page_data and page_data["KeyValuePairs"]:
                formatted.append("### Key Information:\n")
                for key, value in page_data["KeyValuePairs"].items():
                    formatted.append(f"- **{key}**: {value}\n")
        
        return "\n".join(formatted)

