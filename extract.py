#!/usr/bin/env python3
"""
PDF Data Extraction Tool - Main CLI Entry Point

Extracts text, tables, and images from PDF files using Claude 4.5 Sonnet and outputs structured JSON.
"""

import argparse
import json
import sys
from pathlib import Path
from tqdm import tqdm

from pdf_extractor import ClaudeExtractor, MarkdownParser, DataSchematizer


def initialize_directories(output_dir: str = "output"):
    """Initialize output directory structure."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "images").mkdir(exist_ok=True)
    (output_path / "tables").mkdir(exist_ok=True)
    return output_path


def combine_extractions(
    parsed_data: dict,
    schematized_data: dict
) -> dict:
    """
    Combine all extractions into final report structure.
    
    Args:
        parsed_data: Parsed Markdown data (contains text, tables, images)
        schematized_data: Key-value pair extraction results
        
    Returns:
        Combined final report dictionary
    """
    final_report = {}
    
    # Sort page keys numerically
    sorted_page_keys = sorted(
        parsed_data.keys(),
        key=lambda x: int(x.split('_')[1]) if '_' in x else 0
    )
    
    # Combine data for each page
    for page_key in sorted_page_keys:
        page_data = parsed_data.get(page_key, {})
        final_report[page_key] = {
            "Text Content": page_data.get("Text Content", []),
            "Table References": page_data.get("Table References", []),
            "Image References": page_data.get("Image References", []),
            "KeyValuePairs": schematized_data.get(page_key, {})
        }
    
    return final_report


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract text, tables, and images from PDF files and output structured JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py --input sample.pdf
  python extract.py --input /path/to/document.pdf --output custom_output
        """
    )
    
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input PDF file"
    )
    
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory (default: output)"
    )
    
    parser.add_argument(
        "--config",
        default=None,
        help="Path to patterns.json config file (default: config/patterns.json)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.input)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Warning: File does not have .pdf extension: {pdf_path}", file=sys.stderr)
    
    # Initialize output directories
    output_dir = args.output
    initialize_directories(output_dir)
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    try:
        # Initialize Claude extractor and parser
        claude_extractor = ClaudeExtractor(output_dir=output_dir)
        markdown_parser = MarkdownParser(output_dir=output_dir)
        schematizer = DataSchematizer(config_path=args.config, output_dir=output_dir)
        
        # Convert PDF to Markdown using Claude
        print("Converting PDF to Markdown using Claude 4.5 Sonnet...")
        with tqdm(total=1, desc="Claude extraction", unit="file") as pbar:
            markdown = claude_extractor.extract(str(pdf_path))
            pbar.update(1)
        
        # Save Markdown to output.md
        markdown_file = Path(output_dir) / "output.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  ✓ Markdown saved to: {markdown_file}")
        
        # Parse Markdown into structured format
        print("Parsing Markdown...")
        with tqdm(total=1, desc="Markdown parsing", unit="file") as pbar:
            parsed_data = markdown_parser.parse_markdown_to_pages(markdown, pdf_path.stem)
            pbar.update(1)
        
        print(f"  ✓ Parsed {len(parsed_data)} page(s)")
        
        # Extract text for schematizer
        all_text = []
        for page_key, page_data in parsed_data.items():
            for text_item in page_data.get("Text Content", []):
                if isinstance(text_item, dict):
                    all_text.append(text_item.get("text", ""))
        full_text = " ".join(all_text)
        
        # Apply schematizer
        print("Applying data schematizer...")
        schematized_data = {}
        if full_text:
            kv_pairs = schematizer.extract(full_text)
            # Distribute key-value pairs across pages
            for page_key in parsed_data.keys():
                schematized_data[page_key] = kv_pairs
        
        total_kv_pairs = sum(len(kv) for kv in schematized_data.values())
        print(f"  ✓ Extracted {total_kv_pairs} key-value pair(s)")
        
        # Count tables and images
        total_tables = sum(len(page_data.get("Table References", [])) for page_data in parsed_data.values())
        total_images = sum(len(page_data.get("Image References", [])) for page_data in parsed_data.values())
        print(f"  ✓ Found {total_tables} table(s) and {total_images} image reference(s)")
        
        # Combine all extractions
        print("Combining results...")
        final_report = combine_extractions(parsed_data, schematized_data)
        
        # Save final report
        output_file = Path(output_dir) / "final_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print("-" * 60)
        print(f"✓ Extraction complete!")
        print(f"  Final report saved to: {output_file}")
        print(f"  Markdown saved to: {markdown_file}")
        print(f"  Tables saved to: {Path(output_dir) / 'tables'}")
        print(f"  Images saved to: {Path(output_dir) / 'images'}")
        
    except KeyboardInterrupt:
        print("\n\nExtraction interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError during extraction: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

