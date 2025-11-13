#!/usr/bin/env python3
"""
Test script to verify translation system setup
"""

import sys

def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing imports...")

    try:
        import fitz
        print("  ✓ PyMuPDF (fitz)")
    except ImportError as e:
        print(f"  ✗ PyMuPDF: {e}")
        return False

    try:
        from PIL import Image
        print("  ✓ Pillow (PIL)")
    except ImportError as e:
        print(f"  ✗ Pillow: {e}")
        return False

    try:
        import pytesseract
        print("  ✓ pytesseract")
    except ImportError as e:
        print(f"  ✗ pytesseract: {e}")
        return False

    try:
        from deep_translator import GoogleTranslator
        print("  ✓ deep-translator")
    except ImportError as e:
        print(f"  ✗ deep-translator: {e}")
        return False

    return True

def test_tesseract():
    """Test if Tesseract is installed and has Thai support"""
    print("\nTesting Tesseract...")

    import subprocess

    try:
        # Check if tesseract command exists
        result = subprocess.run(['tesseract', '--version'],
                              capture_output=True, text=True)
        print(f"  ✓ Tesseract installed: {result.stdout.split()[1]}")
    except FileNotFoundError:
        print("  ✗ Tesseract not found. Install with: sudo apt-get install tesseract-ocr")
        return False

    try:
        # Check for Thai language support
        result = subprocess.run(['tesseract', '--list-langs'],
                              capture_output=True, text=True)
        if 'tha' in result.stdout:
            print("  ✓ Thai language support available")
            return True
        else:
            print("  ✗ Thai language pack not found. Install with: sudo apt-get install tesseract-ocr-tha")
            return False
    except Exception as e:
        print(f"  ✗ Error checking languages: {e}")
        return False

def test_translation():
    """Test if translation API works"""
    print("\nTesting translation API...")

    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='th', target='en')

        # Test translation
        thai_text = "สวัสดี"
        english_text = translator.translate(thai_text)

        print(f"  Test: '{thai_text}' → '{english_text}'")
        print("  ✓ Translation API working")
        return True
    except Exception as e:
        print(f"  ✗ Translation failed: {e}")
        print("  Check internet connection")
        return False

def test_pdf_access():
    """Test if PDF files are accessible"""
    print("\nChecking PDF files...")

    import os

    pdf_files = [
        "Kammacatukka & Maraṇuppatticatukka.pdf",
        "Vithisangaha.pdf",
        "Bhumicatukka & Patisandhicatukka,.pdf"
    ]

    all_found = True
    for pdf in pdf_files:
        if os.path.exists(pdf):
            size = os.path.getsize(pdf) / (1024*1024)
            print(f"  ✓ {pdf} ({size:.1f} MB)")
        else:
            print(f"  ✗ {pdf} not found")
            all_found = False

    return all_found

def main():
    print("="*70)
    print("Abhidhamma Translation System - Setup Test")
    print("="*70)

    results = []

    # Run tests
    results.append(("Python Libraries", test_imports()))
    results.append(("Tesseract OCR", test_tesseract()))
    results.append(("Translation API", test_translation()))
    results.append(("PDF Files", test_pdf_access()))

    # Summary
    print("\n" + "="*70)
    print("Test Summary:")
    print("="*70)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<50} {status}")
        if not passed:
            all_passed = False

    print("="*70)

    if all_passed:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nRun translation with:")
        print("  python translate_abhidhamma.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nFor setup help, see: TRANSLATION_GUIDE.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
