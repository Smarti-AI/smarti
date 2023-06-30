"""test OCR reader"""

import smarti.ocr.ocr_easyocr as easyocr
import smarti.ocr.ocr_tesseract as tesseract


def test_easyocr_reader(input_folder):
    """test image to OCR translate"""
    results = []

    easyocr.reader = easyocr.recreate_reader(["en"])

    with open(input_folder + "formula1.png", "rb") as file:
        results.append(easyocr.read_text(file.read()))
        print(results[-1])

    with open(input_folder + "question.png", "rb") as file:
        results.append(easyocr.read_text(file.read()))
        print(results[-1])

    assert len(results) == 2


def test_tesseract_reader(input_folder):
    """test tesseract OCR"""
    results = []
    with open(input_folder + "formula1.png", "rb") as file:
        results.append(tesseract.read_text(file.read()))
        print(results[-1])

    with open(input_folder + "question.png", "rb") as file:
        results.append(tesseract.read_text(file.read()))
        print(results[-1])

    with open(input_folder + "heb-question.png", "rb") as file:
        results.append(tesseract.read_text(file.read(), "heb"))
        print(results[-1])

    assert len(results) == 3
