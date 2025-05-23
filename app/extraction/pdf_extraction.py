# --- pdf_extraction.py ---

from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import os

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Failed to open {pdf_path.name}: {e}")
        return ""

    full_text = ""

    for page_number, page in enumerate(doc, start=1):
        try:
            page_text = page.get_text()
            if not page_text.strip():
                # If no text found, fallback to enhanced OCR
                pix = page.get_pixmap(dpi=400)  # Higher DPI
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Preprocess image for better OCR
                img = ImageOps.grayscale(img)
                img = ImageOps.autocontrast(img)
                img = ImageEnhance.Sharpness(img).enhance(2.0)

                ocr_text = pytesseract.image_to_string(img)
                full_text += ocr_text + "\n"
            else:
                full_text += page_text + "\n"
        except Exception as e:
            print(f"Failed to extract page {page_number} of {pdf_path.name}: {e}")

    return full_text

if __name__ == "__main__":
    extraction_script_path = Path(__file__).resolve()
    app_folder = extraction_script_path.parent  # Assuming inside `/extraction/`

    data_folder = app_folder.parent / "data"
    output_folder = app_folder.parent / "extracted_texts"
    output_folder.mkdir(parents=True, exist_ok=True)

    for pdf_file in data_folder.rglob("*.pdf"):
        company_name = pdf_file.parent.name.replace(" ", "_")
        pdf_name = pdf_file.stem.replace(" ", "_")
        output_filename = f"{company_name}_{pdf_name}.txt"
        output_file = output_folder / output_filename

        if output_file.exists():
            print(f"Skipping already extracted file: {output_filename}")
            continue

        print(f"Processing {pdf_file.name}")
        text = extract_text_from_pdf(pdf_file)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Extracted: {output_filename}")

    print("Text extraction completed.")
