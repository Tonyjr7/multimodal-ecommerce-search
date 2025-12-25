from werkzeug.datastructures.file_storage import FileStorage
import easyocr

import logging

# Configure Logging
logger = logging.getLogger(__name__)

# Initialize EasyOCR at module level
logger.info("Initializing EasyOCR...")
ocr_reader = easyocr.Reader(['en'])
logger.info("EasyOCR initialized successfully")

"""OCR Service(EasyOCR Initialization)"""
def ocr_service(file: FileStorage) -> str:
    """
    Processes an uploaded image to extract text using EasyOCR.

    Args:
        file (FileStorage): The image file uploaded by the user.

    Returns:
        str: The extracted text from the image.
    """
    try:
        # Read file bytes
        file_bytes = file.read()
        
        # expected result format: [[bbox, text, conf], [bbox, text, conf]]
        result = ocr_reader.readtext(file_bytes)
        
        # Combine all detected words into one sentence
        detected_text = " ".join([res[1] for res in result])

        if not detected_text:
            logger.warning("No text detected in the image")
            return ""
        
        return detected_text
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        return ""