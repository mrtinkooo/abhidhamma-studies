#!/usr/bin/env python3
"""
Abhidhamma PDF Thai to English Translator
Extracts text from scanned Thai PDF images and translates to English
Preserves Pali terms where applicable
"""

import os
import sys
from pathlib import Path
import json
from typing import List, Dict, Optional
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip install PyMuPDF")
    import fitz

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image

try:
    import pytesseract
except ImportError:
    print("Installing pytesseract...")
    os.system("pip install pytesseract")
    import pytesseract

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Installing deep-translator...")
    os.system("pip install deep-translator")
    from deep_translator import GoogleTranslator


class AbhidhammaTranslator:
    """Translator for Thai Abhidhamma texts with Pali term preservation"""

    # Common Pali terms in Abhidhamma (expandable)
    PALI_TERMS = [
        'citta', 'cetasika', 'rupa', 'nibbana', 'kamma', 'vipaka', 'kiriya',
        'kusala', 'akusala', 'abyakata', 'sobhana', 'asobhana',
        'kamavacara', 'rupavacara', 'arupavacara', 'lokuttara',
        'vedana', 'sanna', 'sankhara', 'vinnana', 'phassa',
        'lobha', 'dosa', 'moha', 'alobha', 'adosa', 'amoha',
        'vithi', 'javana', 'tadalarammana', 'bhavanga', 'avajjana',
        'patisandhi', 'bhumi', 'catukka', 'sangaha',
        'dhamma', 'anicca', 'dukkha', 'anatta', 'sati',
        'samadhi', 'panna', 'sila', 'ariya', 'magga', 'phala',
        'sotapanna', 'sakadagami', 'anagami', 'arahant',
        'jhana', 'samapatti', 'arupa', 'metta', 'karuna',
        'mudita', 'upekkha', 'raga', 'ditthi', 'mana',
        'vicikiccha', 'thina', 'middha', 'uddhacca', 'kukkucca',
        'ahirika', 'anottappa', 'viriya', 'adhimokkha',
        'khandha', 'ayatana', 'dhatu', 'sacca', 'indriya',
        'paramattha', 'sammuti', 'pannatti', 'nana', 'vijja',
        'samatha', 'vipassana', 'sankappa', 'vacca', 'kammanta',
        'ajiva', 'vayama', 'smrti', 'paccaya', 'hetu',
        'nama', 'namarupa', 'arammana', 'dvara', 'vipallasa',
        'marana', 'upapatti', 'cuti', 'abhidhamma', 'sutta', 'vinaya',
    ]

    def __init__(self, pdf_path: str, output_dir: str = "translations"):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize translator
        self.translator = GoogleTranslator(source='th', target='en')

        # Base name for output files
        self.base_name = self.pdf_path.stem

    def extract_text_from_page(self, page_image: Image.Image) -> str:
        """Extract Thai text from page image using OCR"""
        try:
            # Use Tesseract with Thai language
            # You may need to install Thai language data: sudo apt-get install tesseract-ocr-tha
            text = pytesseract.image_to_string(page_image, lang='tha+eng')
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def identify_pali_terms(self, text: str) -> List[str]:
        """Identify Pali terms in the text"""
        found_terms = []
        text_lower = text.lower()

        for term in self.PALI_TERMS:
            if term.lower() in text_lower:
                found_terms.append(term)

        return list(set(found_terms))

    def translate_text(self, text: str, chunk_size: int = 4500) -> str:
        """Translate Thai text to English in chunks (API has size limits)"""
        if not text.strip():
            return ""

        # Split text into chunks if too long
        if len(text) <= chunk_size:
            try:
                return self.translator.translate(text)
            except Exception as e:
                print(f"Translation error: {e}")
                return f"[Translation failed: {str(e)}]"

        # Process in chunks
        sentences = text.split('\n')
        translated_chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "\n"
            else:
                if current_chunk:
                    try:
                        translated_chunks.append(self.translator.translate(current_chunk))
                    except Exception as e:
                        print(f"Translation error for chunk: {e}")
                        translated_chunks.append(f"[Translation failed]")
                current_chunk = sentence + "\n"

        # Translate remaining chunk
        if current_chunk:
            try:
                translated_chunks.append(self.translator.translate(current_chunk))
            except Exception as e:
                print(f"Translation error for final chunk: {e}")
                translated_chunks.append(f"[Translation failed]")

        return "\n".join(translated_chunks)

    def process_pdf(self, max_pages: Optional[int] = None) -> Dict:
        """Process entire PDF and extract + translate text"""
        print(f"\n{'='*70}")
        print(f"Processing: {self.pdf_path.name}")
        print(f"{'='*70}\n")

        try:
            doc = fitz.open(self.pdf_path)
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return {"error": str(e)}

        total_pages = len(doc)
        pages_to_process = min(max_pages, total_pages) if max_pages else total_pages

        print(f"Total pages: {total_pages}")
        print(f"Processing: {pages_to_process} pages\n")

        results = {
            "source_file": self.pdf_path.name,
            "total_pages": total_pages,
            "processed_pages": pages_to_process,
            "pages": []
        }

        all_pali_terms = set()

        for page_num in range(pages_to_process):
            print(f"Processing page {page_num + 1}/{pages_to_process}...", end=" ")

            page = doc[page_num]

            # Convert page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            img_data = pix.tobytes("png")

            # Open with PIL
            from io import BytesIO
            img = Image.open(BytesIO(img_data))

            # Extract text via OCR
            thai_text = self.extract_text_from_page(img)

            if not thai_text.strip():
                print("No text extracted")
                results["pages"].append({
                    "page": page_num + 1,
                    "thai_text": "",
                    "english_text": "",
                    "pali_terms": []
                })
                continue

            # Identify Pali terms
            pali_terms = self.identify_pali_terms(thai_text)
            all_pali_terms.update(pali_terms)

            # Translate to English
            english_text = self.translate_text(thai_text)

            print(f"✓ Extracted {len(thai_text)} chars, found {len(pali_terms)} Pali terms")

            results["pages"].append({
                "page": page_num + 1,
                "thai_text": thai_text,
                "english_text": english_text,
                "pali_terms": pali_terms
            })

        doc.close()

        results["all_pali_terms"] = sorted(list(all_pali_terms))

        return results

    def save_results(self, results: Dict):
        """Save translation results in multiple formats"""

        # 1. Save as JSON
        json_file = self.output_dir / f"{self.base_name}_translation.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved JSON: {json_file}")

        # 2. Save as readable text
        txt_file = self.output_dir / f"{self.base_name}_translation.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Translation of: {results['source_file']}\n")
            f.write(f"{'='*70}\n\n")

            if 'all_pali_terms' in results and results['all_pali_terms']:
                f.write("Pali Terms Found:\n")
                f.write(", ".join(results['all_pali_terms']))
                f.write("\n\n" + "="*70 + "\n\n")

            for page_data in results['pages']:
                f.write(f"\n--- Page {page_data['page']} ---\n\n")

                if page_data.get('pali_terms'):
                    f.write(f"[Pali terms on this page: {', '.join(page_data['pali_terms'])}]\n\n")

                f.write("THAI TEXT:\n")
                f.write(page_data['thai_text'])
                f.write("\n\nENGLISH TRANSLATION:\n")
                f.write(page_data['english_text'])
                f.write("\n\n" + "-"*70 + "\n")

        print(f"✓ Saved Text: {txt_file}")

        # 3. Save English-only version
        eng_file = self.output_dir / f"{self.base_name}_english.txt"
        with open(eng_file, 'w', encoding='utf-8') as f:
            f.write(f"English Translation of: {results['source_file']}\n")
            f.write(f"{'='*70}\n\n")

            for page_data in results['pages']:
                if page_data['english_text'].strip():
                    f.write(f"[Page {page_data['page']}]\n")
                    f.write(page_data['english_text'])
                    f.write("\n\n")

        print(f"✓ Saved English: {eng_file}")


def main():
    """Main function to process PDFs"""

    # Find all PDF files in current directory
    pdf_files = [
        "Kammacatukka & Maraṇuppatticatukka.pdf",
        "Vithisangaha.pdf",
        "Bhumicatukka & Patisandhicatukka,.pdf"
    ]

    print("\n" + "="*70)
    print("Abhidhamma Thai to English Translator")
    print("="*70)
    print("\nThis script will:")
    print("1. Extract text from scanned PDF images using OCR")
    print("2. Translate Thai text to English")
    print("3. Identify and preserve Pali terms")
    print("\nNOTE: First run may take time to install dependencies")
    print("      Tesseract Thai language pack is required")
    print("="*70)

    # Check if user wants to process specific file or all
    if len(sys.argv) > 1:
        # Process specific file
        pdf_path = sys.argv[1]
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None

        translator = AbhidhammaTranslator(pdf_path)
        results = translator.process_pdf(max_pages=max_pages)
        translator.save_results(results)
    else:
        # Process all PDFs (with page limit for testing)
        print("\nProcessing all PDF files...")
        print("For full processing, this may take a long time.")

        response = input("\nProcess all pages? (y/n, default=n for first 5 pages): ").strip().lower()
        max_pages = None if response == 'y' else 5

        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                translator = AbhidhammaTranslator(pdf_file)
                results = translator.process_pdf(max_pages=max_pages)
                translator.save_results(results)
                print()

    print("\n" + "="*70)
    print("Translation complete!")
    print(f"Output saved in: ./translations/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
