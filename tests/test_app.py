"""test logic"""

import os
from unittest import mock
from unittest.mock import MagicMock

import pytest
import telebot.apihelper as tg
from smarti.app import telegram_handle_message


def test_index(flask_app, client):
    """test flask_app default"""
    assert flask_app is not None
    res = client.get("/")
    assert res.status_code == 200
    content = res.get_data(as_text=True)
    assert "Smarti" in content


def test_health_check(flask_app, client, mongo_client):
    """test flask_app health check"""
    env = {"MONGO_CONN": "url"}
    create_mongo_patch = "smarti.storage.mongo_client.create_client"

    assert flask_app is not None
    res = client.get("/health")
    assert res.status_code == 500

    with mock.patch.dict(os.environ, env):
        with mock.patch(create_mongo_patch, return_value=mongo_client):
            res = client.get("/health")
            assert res.status_code == 200


def test_webhook_whatsapp(flask_app, client, mocker):
    """test whatsapp webhook"""
    assert flask_app is not None
    assert mocker is not None
    res = client.get("/webhook/whatsapp")
    assert res.status_code == 400
    res = client.post("/webhook/whatsapp")
    assert res.status_code == 415


def test_telegram_message():
    """test telegram loop start"""
    msg = MagicMock()
    msg.text = "Hello"
    with pytest.raises(tg.ApiTelegramException):
        telegram_handle_message(msg)


def test_heroku_boot():
    """test content of boot file"""
    with open("./Procfile", mode="r", encoding="utf-8") as proc_file:
        line = proc_file.readlines()[0]
        parts = line.split(" ")
        assert (
            len(parts) == 3
            and parts[0] == "web:"
            and parts[1] == "gunicorn"
            and parts[2] == "smarti.app:app"
        )
