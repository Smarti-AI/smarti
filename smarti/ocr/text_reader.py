"""read text from image"""

import easyocr


def read(image: bytes, language="en", image_type="png") -> str:
    """open image, perform OCR and return text"""
    reader = easyocr.Reader([language])
    result = reader.readtext(image)
    return result
