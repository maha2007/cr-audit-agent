# PDF Data Extraction Tool

A robust Python tool for extracting text, tables, and images from PDF documents with intelligent key-value pair detection.

## Features

- **Text Extraction**: Extracts text with hierarchy preservation (headings vs body) using font-size analysis
- **Table Extraction**: Detects and extracts tables, exports to CSV and JSON
- **Image Extraction**: Extracts all images and saves them with references
- **Data Schematization**: Identifies key-value pairs using configurable regex patterns and spaCy NER
- **OCR Detection**: Automatically detects scanned pages that require OCR
- **Progress Tracking**: Visual progress bars using tqdm
- **Robust Error Handling**: Comprehensive logging and graceful error handling

## Requirements

- Python 3.10+
- See `requirements.txt` for dependencies

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Basic Usage

```bash
python extract.py --input sample.pdf
```

### Advanced Usage

```bash
# Specify custom output directory
python extract.py --input document.pdf --output custom_output

# Use custom patterns configuration
python extract.py --input document.pdf --config path/to/patterns.json
```

### Command Line Arguments

- `--input` (required): Path to the input PDF file
- `--output` (optional): Output directory (default: `output`)
- `--config` (optional): Path to patterns.json config file (default: `config/patterns.json`)

## Output Structure

The tool creates the following structure:

```
output/
├── images/              # Extracted images (PNG/JPG)
├── tables/              # CSV files for each extracted table
├── final_report.json    # Main output with all extracted data
└── extraction.log       # Log file with extraction details
```

### Output Format

The `final_report.json` file contains structured data per page:

```json
{
  "Page_1": {
    "Text Content": [
      {"type": "heading", "text": "Invoice", "font_size": 14.0},
      {"type": "body", "text": "Invoice details...", "font_size": 10.0}
    ],
    "Table References": [
      {
        "table_id": "Page_1_Table_1",
        "csv_path": "output/tables/Page_1_Table_1.csv",
        "data": [...],
        "rows": 10,
        "columns": 5
      }
    ],
    "Image References": [
      {
        "page": 1,
        "image_path": "output/images/Page_1_Image_1.png",
        "image_index": 1,
        "format": "png"
      }
    ],
    "KeyValuePairs": {
      "Invoice Number": "INV-123",
      "Date": "2024-01-15",
      "Total Amount": "1000.00"
    }
  }
}
```

## Configuration

### Custom Patterns

Edit `config/patterns.json` to add custom regex patterns for key-value extraction:

```json
{
  "patterns": {
    "Custom Field": [
      "pattern1:?\\s*(\\w+)",
      "pattern2:?\\s*(\\d+)"
    ]
  },
  "ner_labels": ["DATE", "MONEY", "ORG", "PERSON", "GPE"]
}
```

## Architecture

The tool uses a modular OOP design:

- `BaseExtractor`: Base class with common functionality
- `TextExtractor`: Text extraction with Docling (PyMuPDF fallback)
- `TableExtractor`: Table extraction using pdfplumber
- `ImageExtractor`: Image extraction using PyMuPDF
- `DataSchematizer`: Key-value pair extraction using regex and NER

## Libraries Used

- **Docling**: ML-based document understanding (primary for text)
- **PyMuPDF (fitz)**: PDF processing and image extraction
- **pdfplumber**: Table extraction from complex layouts
- **pandas**: Table data management
- **spaCy**: Named Entity Recognition for key-value extraction
- **tqdm**: Progress bars

## Error Handling

- Scanned pages (no selectable text) are logged as "OCR Required"
- Missing libraries gracefully fall back to alternatives
- All errors are logged to `output/extraction.log`
- Invalid PDFs are detected and reported

## License

This project is provided as-is for PDF data extraction purposes.

