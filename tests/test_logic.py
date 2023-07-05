"""test logic"""

from smarti.logic import whatsapp
import smarti.logic.facade as pf


def handle_whatsapp_message(body):
    """handle whatsapp message"""
    assert whatsapp.handle_whatsapp_message(body) == ""


def handle_audio_message():
    """handle audio message"""
    # pylint: disable=no-value-for-parameter
    assert whatsapp.handle_audio_message() == ""


def test_upload_workbook():
    """test workbook upload"""
    body = b""
    assert pf.upload_workbook(body) == 0


def test_send_message():
    """test chat"""
    assert pf.send_message("") == ""
