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
            Combined extraction data dictionary
        """
        all_extractions = {}
        combined_data = {
            "obligor_name": obligor_name,
            "outstanding_limit": outstanding_limit,
            "documents": []
        }
        
        # Initialize Claude extractor and parser
        claude_extractor = ClaudeExtractor(output_dir=str(self.output_dir))
        markdown_parser = MarkdownParser(output_dir=str(self.output_dir))
        schematizer = DataSchematizer(output_dir=str(self.output_dir))
        
        for idx, pdf_file in enumerate(pdf_files):
            # Handle different file input types
            if hasattr(pdf_file, 'name'):  # Streamlit UploadedFile
                pdf_path = self._save_uploaded_file(pdf_file, idx)
                doc_name = pdf_file.name
            elif isinstance(pdf_file, (str, Path)):  # File path
                pdf_path = Path(pdf_file)
                doc_name = pdf_path.name
            else:
                continue
            
            if not pdf_path.exists():
                continue
            
            # Extract from PDF using Claude
            try:
                # Step 1: Convert PDF to Markdown using Claude
                markdown = claude_extractor.extract(str(pdf_path))
                
                # Step 2: Parse Markdown into structured format
                parsed_data = markdown_parser.parse_markdown_to_pages(markdown, doc_name)
                
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
                    kv_pairs = schematizer.extract(full_text)
                    # Distribute key-value pairs across pages (or keep at document level)
                    for page_key in parsed_data.keys():
                        schematized_data[page_key] = kv_pairs
                
                # Step 5: Combine extractions for this document
                doc_data = self._combine_extractions(
                    parsed_data, schematized_data, doc_name
                )
                
                combined_data["documents"].append({
                    "document_name": doc_name,
                    "pages": doc_data
                })
                
            except Exception as e:
                # Log error but continue with other PDFs
                print(f"Error processing {doc_name}: {e}")
                import traceback
                traceback.print_exc()
                continue
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

