"""test logic"""

from smarti.logic import whatsapp


def handle_whatsapp_message(body):
    """handle whatsapp message"""
    assert whatsapp.handle_whatsapp_message(body) == ""


def handle_audio_message():
    """handle audio message"""
    # pylint: disable=no-value-for-parameter
    assert whatsapp.handle_audio_message() == ""
