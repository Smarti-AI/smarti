"""telegram bot class"""

import threading
import telebot


# pylint: disable=too-few-public-methods
class TelegramBot:
    """telegram bot class"""

    def __init__(self, token) -> None:
        """init bot and polling"""
        self.bot = telebot.TeleBot(token)
        self.daemon = threading.Thread(target=self.bot.infinity_polling, daemon=True)
        self.daemon.start()

    def stop(self):
        """stop bot"""
        self.bot.stop_bot()
