"""test logic"""

from smarti.logic.bot import onboarding
from smarti.logic import db


def test_save_new_message():
    """handle whatsapp message"""
    messages = db.load_messages()
    message = onboarding.get_next_message(messages)
    db.save_new_bot_message(message)
