"""read text from image by using tesseract

TODO: check if we need to reverse string from RTL scripts
def reverse_string(str_lines: str) -> str:
    lines = str_lines.split("\n")
    lines = [line[::-1] for line in lines]
    return "\n".join(lines)

def is_rtl_script(lang: str) -> bool:
    return lang.strip() in {"ara", "heb", "fas", "urd", "pus"}
"""

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
    """create temp file for image"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image)
    return tmp.name
