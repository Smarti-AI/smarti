"""flask app runner"""
import os
import sys
import logging
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# smarti imports
from smarti.logic import whatsapp
import smarti.storage.mongo_client as mongo
import smarti.transport.telegram.telegram_bot as tb


# we need to go one level up to import from the root, since the sources are under smarti path
dotenv_path = join(dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

app = Flask(__name__, static_url_path="/static")
log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))

telegram = tb.TelegramBot(os.environ["TELEGRAM_TOKEN"])


@app.route("/")
def hello_world():
    """default flask handler"""
    log.info("hello_world invoked")
    return app.send_static_file("index.html")


@app.route("/health", methods=["GET"])
def health_check():
    """default flask handler"""
    try:
        mongo_conn = os.environ["MONGO_CONN"]
        log.info("mongo conn %s", mongo_conn.split("@")[-1])
        client = mongo.create_client(mongo_conn)
        info = client.server_info()
        log.info("Mongo Health Check %s", list(info.keys()))

        assert telegram.bot_running
        log.info("Telegram bot is running %s", telegram.bot_running)

        return "OK", 200
    except Exception:  # pylint: disable=broad-except
        log.exception("Health Check failed")
        return "Fail", 500


# Accepts POST and GET requests at /webhook/whatsapp endpoint
@app.route("/webhook/whatsapp", methods=["POST", "GET"])
def webhook():
    """WhatsApp webhook handler"""
    if request.method == "GET":
        return whatsapp.verify(request, whatsapp.get_whatsapp_verify_token())
    if request.method == "POST":
        return whatsapp.handle_message(request)
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@telegram.bot.message_handler(func=lambda _: True)
def telegram_handle_message(message):
    """reply to all messages in telegram"""
    return telegram.bot.reply_to(message, f"Smarti replied: {message.text}")


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 8888))
    app.run(debug=True, host="0.0.0.0", port=port)
    telegram.stop()
