"""read text from image by using tesseract"""

import os
import tempfile
from PIL import Image
import pytesseract as ocr


def read_text(image: bytes, lang="eng") -> str:
    """open image, perform OCR and return text by using easy"""
    name = create_temp_file(image)
    res = ocr.image_to_string(Image.open(name), lang=lang)
    os.remove(name)
    return res


def create_temp_file(image: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image)
    return tmp.name
