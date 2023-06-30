"""test OCR reader"""

import smarti.ocr.ocr_easyocr as easyocr
import smarti.ocr.ocr_tesseract as tesseract


def test_easyocr_reader(input_folder):
    """test image to OCR translate"""
    results = []

    reader = easyocr.create_reader(["en"])

    with open(input_folder + "formula1.png", "rb") as file:
        results.append(easyocr.read_text(file.read(), reader=reader))
        print(results[-1])

    with open(input_folder + "question.png", "rb") as file:
        results.append(easyocr.read_text(file.read(), reader=reader))
        print(results[-1])

    assert len(results) == 2


def test_tesseract_reader(input_folder):
    """test tesseract OCR"""
    with open(input_folder + "formula1.png", "rb") as file:
        text = tesseract.read_text(file.read())
        assert "4x* —5x-12=0" == text.strip()

    with open(input_folder + "question.png", "rb") as file:
        lines = tesseract.read_text(file.read()).split("\n")
        assert (
            lines[0] == "Sample Question: Which expression is equivalent to 9x2 - 16y2?"
        )
        assert lines[1] == ""
        assert lines[2] == "A. (3x - 4y) (3x - 4y)"
        assert lines[3] == "B. (3x + 4y) (3x + 4y)"
        assert lines[4] == "C. (3x + 4y) (3x - 4y)"
        assert lines[5] == "D. (3x - 4y)?"

    with open(input_folder + "heb-question.png", "rb") as file:
        lines = tesseract.read_text(file.read(), "heb").split("\n")
        print("\n".join(lines))
        assert (
            lines[0].strip() == "1. לְרון הָיוּ 6 קוּפְסָאוּת וּבְכל קוּפְסָא 4 גוּלות."
        )
        assert lines[1].strip() == ""
        assert lines[2].strip() == "כָּמַה גוּלוּת יָש לְרוּן?"
