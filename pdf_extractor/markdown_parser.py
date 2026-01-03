"""
Markdown Parser
Parses Claude's Markdown output into structured format matching existing extraction output.
"""

import re
import csv
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


class MarkdownParser:
    """Parse Markdown output from Claude into structured extraction format."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize Markdown parser.
        
        Args:
            output_dir: Output directory for saving CSV files
        """
        self.output_dir = Path(output_dir)
        (self.output_dir / "tables").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "images").mkdir(parents=True, exist_ok=True)
    
    def parse_markdown_to_pages(self, markdown: str, document_name: str = "document") -> Dict[str, Any]:
        """
        Parse Markdown into page-by-page structured format.
        
        Args:
            markdown: Markdown string from Claude
            document_name: Name of the document
            
        Returns:
            Dictionary with page-by-page structured data matching existing format
        """
        # Split into pages (try to detect page breaks)
        pages = self._split_into_pages(markdown)
        
        result = {}
        
        for page_num, page_content in enumerate(pages, start=1):
            page_key = f"Page_{page_num}"
            
            # Extract text content (headings and body)
            text_content = self._extract_text_content(page_content)
            
            # Extract tables
            table_references = self._extract_tables(page_content, page_key, document_name)
            
            # Extract image references
            image_references = self._extract_images(page_content, page_num)
            
            result[page_key] = {
                "Text Content": text_content,
                "Table References": table_references,
                "Image References": image_references
            }
        
        return result
    
    def _split_into_pages(self, markdown: str) -> List[str]:
        """
        Split Markdown into pages.
        
        Args:
            markdown: Full Markdown content
            
        Returns:
            List of page content strings
        """
        # Try to find page markers (page numbers, page breaks)
        page_patterns = [
            r'---\s*Page\s+(\d+)\s*---',
            r'Page\s+(\d+)',
            r'^\s*#+\s*Page\s+(\d+)',
        ]
        
        # Try to split by page markers
        for pattern in page_patterns:
            matches = list(re.finditer(pattern, markdown, re.IGNORECASE | re.MULTILINE))
            if matches:
                pages = []
                last_pos = 0
                for match in matches:
                    if match.start() > last_pos:
                        pages.append(markdown[last_pos:match.start()])
                        last_pos = match.start()
                if last_pos < len(markdown):
                    pages.append(markdown[last_pos:])
                if pages:
                    return pages
        
        # If no page markers found, split by approximate content length
        # or treat as single page
        # For now, treat as single page - can be improved later
        return [markdown]
    
    def _extract_text_content(self, markdown: str) -> List[Dict[str, Any]]:
        """
        Extract text content with hierarchy (headings vs body).
        
        Args:
            markdown: Markdown content for a page
            
        Returns:
            List of text items with type and text
        """
        text_items = []
        lines = markdown.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's a heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                text_items.append({
                    "type": "heading",
                    "text": heading_match.group(2).strip(),
                    "font_size": None  # No font size info from Markdown
                })
            # Check if it's a table (skip, handled separately)
            elif line.startswith('|') and '|' in line[1:]:
                continue
            # Check if it's an image placeholder (skip, handled separately)
            elif re.match(r'^\[(?:Chart|Image):', line):
                continue
            # Regular body text
            else:
                if line:
                    text_items.append({
                        "type": "body",
                        "text": line,
                        "font_size": None
                    })
        
        return text_items
    
    def _extract_tables(self, markdown: str, page_key: str, document_name: str) -> List[Dict[str, Any]]:
        """
        Extract tables from Markdown.
        
        Args:
            markdown: Markdown content
            page_key: Page identifier (e.g., "Page_1")
            document_name: Document name
            
        Returns:
            List of table references matching existing format
        """
        tables = []
        
        # Find all Markdown tables
        # Markdown table pattern: | col1 | col2 | ... |
        table_pattern = r'\|[^\n]+\|\n(?:\|[-:\s]+\|\n)?(?:\|[^\n]+\|\n?)+'
        table_matches = re.finditer(table_pattern, markdown, re.MULTILINE)
        
        table_index = 1
        for match in table_matches:
            table_markdown = match.group(0)
            
            # Parse table into rows
            rows = []
            for line in table_markdown.strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('|--'):
                    continue
                
                # Extract cells
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells:
                    rows.append(cells)
            
            if not rows:
                continue
            
            # First row is header
            headers = rows[0] if rows else []
            data_rows = rows[1:] if len(rows) > 1 else []
            
            # Create DataFrame
            if headers:
                df = pd.DataFrame(data_rows, columns=headers)
            else:
                df = pd.DataFrame(data_rows)
            
            # Generate table ID
            table_id = f"{page_key}_Table_{table_index}"
            table_index += 1
            
            # Save as CSV
            csv_path = self.output_dir / "tables" / f"{table_id}.csv"
            df.to_csv(csv_path, index=False)
            
            # Convert to dict format for JSON
            table_data = df.to_dict('records')
            raw_data = df.values.tolist()
            
            # Calculate relative path
            if not csv_path.is_absolute():
                csv_path_str = str(csv_path)
            else:
                try:
                    csv_path_str = str(csv_path.relative_to(Path.cwd()))
                except (ValueError, TypeError):
                    try:
                        csv_path_str = str(csv_path.relative_to(self.output_dir.parent))
                    except (ValueError, TypeError):
                        csv_path_str = str(csv_path)
            
            tables.append({
                "table_id": table_id,
                "csv_path": csv_path_str,
                "data": table_data,
                "raw_data": raw_data,
                "rows": len(df),
                "columns": len(df.columns)
            })
        
        return tables
    
    def _extract_images(self, markdown: str, page_num: int) -> List[Dict[str, Any]]:
        """
        Extract image/chart references from Markdown.
        
        Args:
            markdown: Markdown content
            page_num: Page number
            
        Returns:
            List of image references
        """
        images = []
        
        # Find image placeholders: [Chart: ...] or [Image: ...]
        image_pattern = r'\[(?:Chart|Image):\s*([^\]]+)\]'
        matches = re.finditer(image_pattern, markdown, re.IGNORECASE)
        
        image_index = 1
        for match in matches:
            description = match.group(1)
            image_path = match.group(0)  # Full placeholder text
            
            images.append({
                "page": page_num,
                "image_path": image_path,
                "image_index": image_index,
                "format": "placeholder"
            })
            image_index += 1
        
        return images

