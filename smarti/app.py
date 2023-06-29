"""flask app runner"""
import logging
import os
import sys
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, jsonify, request

# smarti imports
from smarti.logic import whatsapp

# sys.path.append("/usr/bin/ffmpeg")
# sys.path.append("/usr/bin/ffprobe")

# we need to go one level up to import from the root, since the sources are under smarti path
dotenv_path = join(dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

app = Flask(__name__, static_url_path="/static")
log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


@app.route("/")
def hello_world():
    """default flask handler"""
    log.info("hello_world invoked")
    return app.send_static_file("index.html")


# Accepts POST and GET requests at /webhook/whatsapp endpoint
@app.route("/webhook/whatsapp", methods=["POST", "GET"])
def webhook():
    """WhatsApp webhook handler"""
    if request.method == "GET":
        return whatsapp.verify(request, whatsapp.get_whatsapp_verify_token())
    if request.method == "POST":
        return whatsapp.handle_message(request)
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 8888))
    app.run(debug=True, host="0.0.0.0", port=port)
