"""read text from image"""

import easyocr


ocr_reader = easyocr.Reader(["en"])


def recreate_reader(language: list) -> easyocr.Reader:
    """Recreate reader with a given lang set"""
    return easyocr.Reader(language)


def read_text(image: bytes, reader: easyocr.Reader = ocr_reader) -> str:
    """open image, perform OCR and return text by using easy"""
    result = reader.readtext(image)
    return merge_rectangles_to_lines(result)


def merge_rectangles_to_lines(rectangles: list) -> list:
    """Merge easy_ocr rectangles to lines"""
    lines = {}
    for rectangle in rectangles:
        left_corner_y = rectangle[0][0][1]
        words = lines.get(left_corner_y, [])
        words.append(rectangle[1])
        lines[left_corner_y] = words

    return list(lines.values())
