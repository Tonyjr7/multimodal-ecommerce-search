from PIL import Image
import pytesseract 


def ocr_core(file):
    # 1. Read Image for OCR
    img = Image.open(file.stream)
    
    # 2. Run Tesseract
    # We assume standard English text
    detected_text = pytesseract.image_to_string(img)
    
    # Clean up text (remove newlines)
    detected_text = detected_text.replace('\n', ' ').strip()

    return detected_text