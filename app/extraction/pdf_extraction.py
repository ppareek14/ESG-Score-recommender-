# --- pdf_extraction.py ---
from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import json

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    output = []

    for page_number, page in enumerate(doc, start=1):
        try:
            text = page.get_text().strip()
            if not text:
                pix = page.get_pixmap(dpi=400)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = ImageOps.grayscale(img)
                img = ImageOps.autocontrast(img)
                img = ImageEnhance.Sharpness(img).enhance(2.0)
                text = pytesseract.image_to_string(img).strip()

            if text:
                output.append({"page": page_number, "text": text})
        except Exception as e:
            print(f"Page {page_number} failed: {e}")

    return output

if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parents[1] / "data"
    output_dir = Path(__file__).resolve().parents[1] / "extracted_texts"

    for pdf_file in data_dir.rglob("*.pdf"):
        # Mirror the data/ path structure in extracted_texts/
        relative_path = pdf_file.relative_to(data_dir).with_suffix(".jsonl")
        output_file = output_dir / relative_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_file.exists():
            print(f"Skipping {pdf_file} (already processed)")
            continue

        print(f"Processing {pdf_file}")
        page_texts = extract_text_by_page(pdf_file)

        with open(output_file, "w", encoding="utf-8") as f:
            for entry in page_texts:
                f.write(json.dumps(entry) + "\n")
