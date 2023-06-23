"""test logic"""

from smarti import app


def handle_whatsapp_message(body):
    """handle whatsapp message"""
    assert app.handle_whatsapp_message(body) == ""


def handle_audio_message():
    """handle audio message"""
    # pylint: disable=no-value-for-parameter
    assert app.handle_audio_message() == ""
