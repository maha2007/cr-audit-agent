#!/bin/bash
# Installation script for PDF Data Extraction Tool

echo "Installing PDF Data Extraction Tool dependencies..."
echo ""

# Install core dependencies
pip3 install --user pymupdf pdfplumber pandas tqdm spacy python-dotenv

# Download spaCy language model
echo ""
echo "Downloading spaCy language model..."
python3 -m spacy download en_core_web_sm

echo ""
echo "Installation complete!"
echo ""
echo "Note: If you encounter SSL errors, try:"
echo "  pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pymupdf pdfplumber pandas tqdm spacy python-dotenv"
echo ""
echo "Optional: Install docling for enhanced text extraction:"
echo "  pip3 install --user docling"

