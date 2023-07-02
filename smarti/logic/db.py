"""save and load data from database"""
import logging
import sys

from flask import json

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


def save_new_user_message(message):
    """save a new user message to the database"""
    user_message = {"role": "user", "content": message}
    return __save_new_message(user_message)


def save_new_bot_message(message):
    """save a new bot message to the database"""
    bot_message = {"role": "system", "content": message}
    return __save_new_message(bot_message)


def load_messages():
    """save a new message to the database"""
    log.info("load_messages invoked")

    try:
        with open("messages.json") as json_file:
            messages = json.load(json_file)
    except (FileNotFoundError, Exception):
        messages = []
    return messages


def __save_new_message(message):
    """save a new message to the database"""
    log.info("save_new_message invoked")
    log.info(message)

    messages = load_messages()
    messages.append(message)

    with open("messages.json", "w") as json_file:
        json.dump(messages, json_file)

    return messages
