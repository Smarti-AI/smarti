"""telegram bot class"""

import threading
import telebot


class TelegramBot:
    """telegram bot class"""

    def __init__(self, token) -> None:
        """init bot and polling"""
        self.bot_running = False
        self.bot = telebot.TeleBot(token)
        self.daemon = threading.Thread(target=self.start, daemon=True)
        self.daemon.start()

    def stop(self):
        """stop bot"""
        self.bot.stop_bot()
        self.bot_running = False

    def start(self):
        "start bot"
        self.bot_running = True
        self.bot.infinity_polling()
