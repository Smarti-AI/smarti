"""test OCR reader"""

import smarti.ocr.ocr_easyocr as ocr


def test_text_reader(input_folder):
    """test image to OCR translate"""
    results = []

    ocr.easyocr_reader = ocr.recreate_reader(["en"])

    with open(input_folder + "formula1.png", "rb") as file:
        results.append(ocr.read_text(file.read(), ocr.easyocr_reader))
        print(results[-1])

    with open(input_folder + "question.png", "rb") as file:
        results.append(ocr.read_text(file.read(), ocr.easyocr_reader))
        print(results[-1])

    assert len(results) == 2
