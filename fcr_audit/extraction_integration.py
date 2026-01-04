"""
PDF Extraction Integration
Integrates Claude-based PDF extraction for processing uploaded PDFs.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List
import shutil

from pdf_extractor import ClaudeExtractor, MarkdownParser, DataSchematizer


class ExtractionIntegration:
    """Handles PDF extraction for FCR audit processing."""
    
    def __init__(self, output_dir: str = "uploads"):
        """
        Initialize extraction integration.
        
        Args:
            output_dir: Directory for temporary extraction outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_pdfs(self, pdf_files: List[Any], obligor_name: str = "", outstanding_limit: str = "") -> Dict[str, Any]:
        """
        Process multiple PDF files and combine their extractions.
        
        Args:
            pdf_files: List of uploaded PDF file objects (Streamlit UploadedFile or file paths)
            obligor_name: Name of the obligor
            outstanding_limit: Outstanding limit
            
        Returns:
            Combined extraction data dictionary with 'errors' key if any failures occurred
        """
        all_extractions = {}
        combined_data = {
            "obligor_name": obligor_name,
            "outstanding_limit": outstanding_limit,
            "documents": [],
            "errors": []  # Track errors for better error reporting
        }
        
        # Initialize Claude extractor and parser
        try:
            claude_extractor = ClaudeExtractor(output_dir=str(self.output_dir))
            markdown_parser = MarkdownParser(output_dir=str(self.output_dir))
            schematizer = DataSchematizer(output_dir=str(self.output_dir))
        except Exception as e:
            combined_data["errors"].append(f"Failed to initialize extractors: {str(e)}")
            return combined_data
        
        for idx, pdf_file in enumerate(pdf_files):
            # Handle different file input types
            if hasattr(pdf_file, 'name'):  # Streamlit UploadedFile
                try:
                    pdf_path = self._save_uploaded_file(pdf_file, idx)
                    doc_name = pdf_file.name
                except Exception as e:
                    combined_data["errors"].append(f"Failed to save uploaded file {pdf_file.name}: {str(e)}")
                    continue
            elif isinstance(pdf_file, (str, Path)):  # File path
                pdf_path = Path(pdf_file)
                doc_name = pdf_path.name
            else:
                combined_data["errors"].append(f"Unsupported file type: {type(pdf_file)}")
                continue
            
            if not pdf_path.exists():
                combined_data["errors"].append(f"File not found: {doc_name}")
                continue
            
            # Extract from PDF using Claude
            try:
                # Step 1: Convert PDF to Markdown using Claude
                markdown = claude_extractor.extract(str(pdf_path))
                
                if not markdown or len(markdown.strip()) == 0:
                    combined_data["errors"].append(f"Empty extraction result for {doc_name}. The PDF may be corrupted or unreadable.")
                    continue
                
                # Step 2: Parse Markdown into structured format
                parsed_data = markdown_parser.parse_markdown_to_pages(markdown, doc_name)
                
                if not parsed_data:
                    combined_data["errors"].append(f"Failed to parse Markdown for {doc_name}. The PDF content may not be extractable.")
                    continue
                
                # Step 3: Extract text for schematizer (combine all text from all pages)
                all_text = []
                for page_key, page_data in parsed_data.items():
                    for text_item in page_data.get("Text Content", []):
                        if isinstance(text_item, dict):
                            all_text.append(text_item.get("text", ""))
                full_text = " ".join(all_text)
                
                # Step 4: Apply schematizer to extract key-value pairs
                schematized_data = {}
                if full_text:
                    try:
                        kv_pairs = schematizer.extract(full_text)
                        # Distribute key-value pairs across pages (or keep at document level)
                        for page_key in parsed_data.keys():
                            schematized_data[page_key] = kv_pairs
                    except Exception as e:
                        # Schematizer errors are non-critical, continue without key-value pairs
                        print(f"Warning: Schematizer failed for {doc_name}: {str(e)}")
                
                # Step 5: Combine extractions for this document
                doc_data = self._combine_extractions(
                    parsed_data, schematized_data, doc_name
                )
                
                combined_data["documents"].append({
                    "document_name": doc_name,
                    "pages": doc_data
                })
                
            except FileNotFoundError as e:
                combined_data["errors"].append(f"File not found: {doc_name} - {str(e)}")
            except ValueError as e:
                # API key or configuration errors
                combined_data["errors"].append(f"Configuration error for {doc_name}: {str(e)}")
            except RuntimeError as e:
                # API errors (rate limits, overloaded, etc.)
                error_msg = str(e)
                if "rate_limit" in error_msg.lower() or "overloaded" in error_msg.lower():
                    combined_data["errors"].append(f"Claude API is rate-limited or overloaded. Please try again in a few moments. Error: {str(e)}")
                else:
                    combined_data["errors"].append(f"Claude API error for {doc_name}: {str(e)}")
            except Exception as e:
                # Generic errors
                import traceback
                error_details = traceback.format_exc()
                combined_data["errors"].append(f"Error processing {doc_name}: {str(e)}")
                print(f"Full error traceback for {doc_name}:\n{error_details}")
            finally:
                # Clean up temporary file if it was uploaded
                if hasattr(pdf_file, 'name') and pdf_path.exists():
                    try:
                        pdf_path.unlink()
                    except:
                        pass
        
        return combined_data
    
    def _save_uploaded_file(self, uploaded_file, index: int) -> Path:
        """
        Save uploaded file to temporary location.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            index: File index
            
        Returns:
            Path to saved file
        """
        # Create temporary file
        suffix = Path(uploaded_file.name).suffix
        temp_file = self.output_dir / f"temp_{index}_{uploaded_file.name}"
        
        # Save file
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_file
    
    def _combine_extractions(
        self,
        parsed_data: Dict[str, Any],
        schematized_data: Dict[str, Any],
        doc_name: str
    ) -> Dict[str, Any]:
        """
        Combine all extractions for a single document.
        
        Args:
            parsed_data: Parsed Markdown data (already contains text, tables, images)
            schematized_data: Key-value pair extraction results
            doc_name: Document name
            
        Returns:
            Combined page-by-page data
        """
        combined = {}
        
        # Sort page keys numerically
        sorted_page_keys = sorted(
            parsed_data.keys(),
            key=lambda x: int(x.split('_')[1]) if '_' in x else 0
        )
        
        # Combine data for each page
        for page_key in sorted_page_keys:
            page_data = parsed_data.get(page_key, {})
            combined[page_key] = {
                "document": doc_name,
                "Text Content": page_data.get("Text Content", []),
                "Table References": page_data.get("Table References", []),
                "Image References": page_data.get("Image References", []),
                "KeyValuePairs": schematized_data.get(page_key, {})
            }
        
        return combined
    
    def format_for_gemini(self, combined_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format extraction data for Claude API input.
        
        Note: Method name kept for backward compatibility.
        
        Args:
            combined_data: Combined extraction data
            
        Returns:
            Formatted data for Claude
        """
        # Flatten document structure for easier processing
        formatted = {
            "obligor_name": combined_data.get("obligor_name", ""),
            "outstanding_limit": combined_data.get("outstanding_limit", ""),
            "pages": {}
        }
        
        # Combine all pages from all documents
        page_counter = 1
        for doc in combined_data.get("documents", []):
            doc_name = doc.get("document_name", "Unknown")
            for page_key, page_data in doc.get("pages", {}).items():
                # Renumber pages sequentially across documents
                new_page_key = f"Page_{page_counter}"
                formatted["pages"][new_page_key] = {
                    "document": doc_name,
                    "original_page": page_key,
                    **page_data
                }
                page_counter += 1
        
        return formatted

