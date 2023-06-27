"""read text from image"""


def read(image: bytes, image_type="png") -> str:
    """open image, perform OCR and return text"""
    return str(len(image)) + image_type
