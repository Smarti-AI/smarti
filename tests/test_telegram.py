"""test telegram"""

import time
import smarti.transport.telegram.telegram_bot as tg


def test_telegram_wrapper():
    """test telegram bot wrapper"""
    telegram = tg.TelegramBot("empty")
    time.sleep(1)
    assert telegram.bot_running
    telegram.stop()
    assert not telegram.bot_running
