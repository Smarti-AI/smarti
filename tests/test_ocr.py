"""test OCR reader"""

import smarti.ocr.text_reader as ocr


def test_text_reader(input_folder):
    """test image to OCR translate"""
    fname = input_folder + "formula1.png"
    with open(fname, "rb") as file:
        content = file.read()
        res = ocr.read(content)
        assert not res is None
