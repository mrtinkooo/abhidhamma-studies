#!/bin/bash
# Setup script for Abhidhamma Translation System

echo "=========================================="
echo "Abhidhamma Translation Setup"
echo "=========================================="
echo ""

# Check if Tesseract is installed
echo "Checking for Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    echo "Installing Tesseract OCR..."
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr
else
    echo "✓ Tesseract OCR already installed"
fi

# Install Thai language pack for Tesseract
echo ""
echo "Installing Thai language pack..."
sudo apt-get install -y tesseract-ocr-tha

# Verify Thai language pack
echo ""
echo "Verifying Thai language support..."
tesseract --list-langs | grep tha && echo "✓ Thai language pack installed" || echo "✗ Thai language pack not found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  Process all PDFs (first 5 pages as test):"
echo "    python translate_abhidhamma.py"
echo ""
echo "  Process specific PDF (all pages):"
echo "    python translate_abhidhamma.py 'Vithisangaha.pdf'"
echo ""
echo "  Process specific PDF (limited pages):"
echo "    python translate_abhidhamma.py 'Vithisangaha.pdf' 10"
echo ""
