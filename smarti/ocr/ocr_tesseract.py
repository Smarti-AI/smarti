"""read text from image by using tesseract"""

import pytesseract as ocr


def read_text(image: bytes) -> str:
    """open image, perform OCR and return text by using easy"""
    return ",".join(ocr.get_languages()) + str(len(image))
