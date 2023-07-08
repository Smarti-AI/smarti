"""test telegram"""

import smarti.transport.telegram.telegram_bot as tg


def test_telegram_wrapper():
    """test telegram bot wrapper"""
    telegram = tg.TelegramBot("empty")
    telegram.stop()
    assert telegram.daemon.isDaemon()
