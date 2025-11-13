# Abhidhamma Studies

A collection of Thai Abhidhamma texts with automated translation tools.

## Contents

This repository contains three Abhidhamma texts in PDF format:

1. **Kammacatukka & Maraṇuppatticatukka** (21 MB)
2. **Vithisangaha** (11 MB)
3. **Bhumicatukka & Patisandhicatukka** (16 MB)

## Thai to English Translation System

This repository includes an automated translation system that:
- Extracts text from scanned Thai PDF images using OCR
- Translates Thai text to English
- Identifies and preserves Pali terminology

### Quick Start

1. **Run setup**:
   ```bash
   ./setup_translation.sh
   ```

2. **Test your setup**:
   ```bash
   python test_setup.py
   ```

3. **Translate PDFs**:
   ```bash
   # Test with first 5 pages
   python translate_abhidhamma.py

   # Translate specific book
   python translate_abhidhamma.py "Vithisangaha.pdf"
   ```

### Documentation

See [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) for detailed instructions.

### Requirements

- Python 3.7+
- Tesseract OCR with Thai language support
- Internet connection (for translation)

### Output

Translations are saved in the `translations/` directory in three formats:
- JSON (machine-readable)
- Full bilingual text (Thai + English)
- English-only text

## License

Please acknowledge original sources when using translated texts. Machine translations should be reviewed by scholars for accuracy.