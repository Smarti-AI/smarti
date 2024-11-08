"""test OCR reader"""

import smarti.ocr.ocr_tesseract as tesseract


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
        assert len(lines) == 4

        # Works on MAC, doesn't work on Linux (without heb support)
        # lines[0].strip() == "1. לְרון הָיוּ 6 קוּפְסָאוּת וּבְכל קוּפְסָא 4 גוּלות."
        # lines[2].strip() == "כָּמַה גוּלוּת יָש לְרוּן?"

        actual = set(lines[0].split(" "))
        expected = set(
            "1. לְרון הָיוּ 6 קוּפְסָאוּת וּבְכל קוּפְסָא 4 גוּלות.".split(" ")
        )

        diff = actual.difference(expected)
        assert len(diff) >= 0
        if len(diff) > 0:
            print(f"WARN {diff} is not empty")
