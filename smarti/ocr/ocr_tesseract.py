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
    return reverse_string(res) if is_rtl_script(lang) else res


def create_temp_file(image: bytes) -> str:
    """create temp file for image"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image)
    return tmp.name


def is_rtl_script(lang: str) -> bool:
    """check if language uses right to left style"""
    return lang.strip() in {"ara", "heb", "fas", "urd", "pus"}


def reverse_string(str_lines: str) -> str:
    """reverse lines in rtl language"""
    lines = str_lines.split("\n")
    lines = [line[::-1] for line in lines]
    return "\n".join(lines)
