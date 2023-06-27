"""test OCR reader"""

import smarti.ocr.text_reader as ocr


def test_text_reader():
    """test image to OCR translate"""
    assert ocr.read(bytes("", "ASCII")) == "0png"
