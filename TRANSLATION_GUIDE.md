# Abhidhamma Thai to English Translation System

## Overview

This system extracts Thai text from scanned PDF images and translates it to English while preserving Pali terminology commonly used in Abhidhamma texts.

## Features

1. **OCR Text Extraction**: Uses Tesseract OCR with Thai language support to extract text from scanned images
2. **Thai to English Translation**: Automatically translates Thai text using Google Translate
3. **Pali Term Recognition**: Identifies and tracks common Pali terms used in Abhidhamma literature
4. **Multiple Output Formats**: Generates JSON, full text, and English-only versions

## Prerequisites

### System Requirements

- Python 3.7 or higher
- Tesseract OCR with Thai language support
- Internet connection (for translation API)

## Installation

### Option 1: Automated Setup (Linux/Ubuntu)

```bash
./setup_translation.sh
```

### Option 2: Manual Setup

1. **Install Tesseract OCR**:
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-tha
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   tesseract --list-langs | grep tha
   ```
   You should see "tha" in the list.

## Usage

### Basic Usage

Process all PDFs with default settings (first 5 pages of each as test):
```bash
python translate_abhidhamma.py
```

### Process Specific PDF

Process all pages of a specific PDF:
```bash
python translate_abhidhamma.py "Vithisangaha.pdf"
```

Process limited number of pages:
```bash
python translate_abhidhamma.py "Vithisangaha.pdf" 10
```

### Examples

```bash
# Test with first 5 pages of all PDFs
python translate_abhidhamma.py

# Translate entire Vithisangaha book
python translate_abhidhamma.py "Vithisangaha.pdf"

# Translate first 20 pages of Kammacatukka
python translate_abhidhamma.py "Kammacatukka & Maraṇuppatticatukka.pdf" 20
```

## Output Files

The script creates a `translations/` directory with three files for each PDF:

1. **`[filename]_translation.json`**: Complete data in JSON format
   - Thai text, English translation, Pali terms for each page
   - Machine-readable format for further processing

2. **`[filename]_translation.txt`**: Full bilingual version
   - Both Thai and English text
   - Pali terms highlighted
   - Human-readable format

3. **`[filename]_english.txt`**: English-only version
   - Clean English translation
   - Page numbers preserved

## Pali Terms Recognition

The system recognizes common Abhidhamma Pali terms including:

- **Mental Phenomena**: citta, cetasika, vedana, sanna, sankhara, vinnana
- **Matter**: rupa, namarupa
- **Consciousness Types**: kamavacara, rupavacara, arupavacara, lokuttara
- **Mental Qualities**: kusala, akusala, lobha, dosa, moha, alobha, adosa, amoha
- **Process Terms**: vithi, javana, bhavanga, patisandhi, vipaka, kiriya
- **Path Terms**: magga, phala, jhana, samadhi, panna, sati, vipassana
- And 60+ more terms...

## Customization

### Adding More Pali Terms

Edit `translate_abhidhamma.py` and add terms to the `PALI_TERMS` list in the `AbhidhammaTranslator` class:

```python
PALI_TERMS = [
    'citta', 'cetasika', 'rupa',
    # Add your terms here
    'your_term_1', 'your_term_2',
]
```

### Adjusting Translation Chunk Size

Modify the `chunk_size` parameter in the `translate_text()` method (default: 4500 characters).

### Improving OCR Quality

Adjust the zoom matrix in `process_pdf()` for higher resolution (uses more memory):

```python
pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 3x zoom instead of 2x
```

## Performance Notes

- **Processing Time**: Approximately 30-60 seconds per page (depends on text density and internet speed)
- **Memory Usage**: ~100-200MB per page (with 2x zoom)
- **API Limits**: Uses free Google Translate API with rate limiting - very large documents may require breaks

## Troubleshooting

### "tesseract: command not found"
Install Tesseract: `sudo apt-get install tesseract-ocr`

### "tha" language not found
Install Thai language pack: `sudo apt-get install tesseract-ocr-tha`

### Poor OCR accuracy
- Increase image resolution (adjust zoom matrix)
- Ensure PDF scan quality is good
- Check if Tesseract Thai language data is properly installed

### Translation API errors
- Check internet connection
- Wait a moment and retry (may be rate limited)
- For very large documents, process in smaller batches

### Out of memory errors
- Process fewer pages at a time
- Reduce the zoom matrix (lower resolution)
- Close other applications

## Advanced Usage

### Batch Processing with Progress Tracking

```python
from translate_abhidhamma import AbhidhammaTranslator

pdfs = ["file1.pdf", "file2.pdf", "file3.pdf"]

for pdf in pdfs:
    translator = AbhidhammaTranslator(pdf)
    results = translator.process_pdf(max_pages=None)  # All pages
    translator.save_results(results)
```

### Processing Specific Page Range

Modify the `process_pdf()` method to accept start and end pages:

```python
# In process_pdf method, add parameters:
def process_pdf(self, start_page: int = 0, end_page: Optional[int] = None):
    # Process from start_page to end_page
```

## Books in Repository

1. **Kammacatukka & Maraṇuppatticatukka.pdf** (21MB)
2. **Vithisangaha.pdf** (11MB)
3. **Bhumicatukka & Patisandhicatukka.pdf** (16MB)

## Technical Details

### Dependencies

- **PyMuPDF (fitz)**: PDF rendering and image extraction
- **Pillow**: Image processing
- **pytesseract**: Python wrapper for Tesseract OCR
- **deep-translator**: Translation API interface (uses Google Translate)

### Translation Pipeline

```
PDF → Image Extraction → OCR (Thai) → Pali Term Detection → Translation → Output Files
```

## License & Attribution

When using translated texts, please:
- Acknowledge the original Thai sources
- Note that translations are machine-generated and may require human review
- Verify Pali terms and technical terminology with scholarly sources

## Future Enhancements

Potential improvements:
- Support for other translation services (DeepL, etc.)
- Better Pali term detection using linguistic patterns
- GUI interface
- Parallel processing for faster translation
- Post-editing interface for corrections
- Glossary building from extracted Pali terms
