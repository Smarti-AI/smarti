"""flask app runner"""
import sys

sys.path.append("/usr/bin/ffmpeg")
sys.path.append("/usr/bin/ffprobe")

import io
import logging
import os

import pydub
import requests
import soundfile as sf
import speech_recognition as sr
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_url_path="/static")
log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


# Access token for your WhatsApp business account app
whatsapp_token = 'EAALABLp6AXUBAHEUWJwspczZA9rEQ2R2TRS7lyfxP1vPikjZAsE2x4Ot1IIC1w8xRBRwhc0Sv9fZBSpTf2bCrtjSZBbBjITODS6Vl4AJrBZBH5QazPUPS0xVZAyniWmJlyMsmvPZADmT87c3765RKZB7BiPMlTL5uCPbJqEDmZAYmBxat5P4ZBw2ZAPSDonBlH8m2kcTe5B4zKnKQZDZD'


# Verify Token defined when configuring the webhook
verify_token = os.environ.get("VERIFY_TOKEN", "WHATSAPP-TOKEN-12345678")


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
        return verify(request)
    if request.method == "POST":
        return handle_message(request)

    return jsonify({"status": "error", "message": "Method not allowed"}), 405


# Required webhook verification for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(req):
    """Parse params from the webhook verification request"""
    mode = req.args.get("hub.mode")
    token = req.args.get("hub.verify_token")
    challenge = req.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == verify_token:
            # Respond with 200 OK and challenge token from the request
            log.info("WEBHOOK_VERIFIED")
            return challenge, 200

        # Responds with '403 Forbidden' if verify tokens do not match
        log.info("VERIFICATION_FAILED")
        return jsonify({"status": "error", "message": "Verification failed"}), 403

    # Responds with '400 Bad Request' if verify tokens do not match
    log.info("MISSING_PARAMETER")
    return jsonify({"status": "error", "message": "Missing parameters"}), 400


# handle incoming webhook messages
def handle_message(req):
    """Parse Request body in json format"""
    body = req.get_json()
    log.info("request body: {%s}", body)

    try:
        # info on WhatsApp text message payload:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):
                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200

        # if the request is not a WhatsApp API event, return an error
        return (
            jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
            404,
        )
    # catch all other errors and return an internal server error
    # pylint: disable=broad-except
    except Exception as exception:
        log.info("unknown error: {%s}", exception)
        return jsonify({"status": "error", "message": str(exception)}), 500


# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
    """handle WhatsApp messages of different types"""
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    if message["type"] == "text":
        message_body = message["text"]["body"]
    elif message["type"] == "audio":
        audio_id = message["audio"]["id"]
        message_body = handle_audio_message(audio_id)
    elif message["type"] == "image":
        # image_id = message["image"]["id"]
        message_body = "image messages not yet supported"
    elif message["type"] == "document":
        # document_id = message["document"]["id"]
        message_body = "document messages not yet supported"
    elif message["type"] == "location":
        # latitude = message["location"]["latitude"]
        # longitude = message["location"]["longitude"]
        message_body = "location messages not yet supported"
    elif message["type"] == "contact":
        # contact_id = message["contact"]["id"]
        message_body = "contact messages not yet supported"
    elif message["type"] == "sticker":
        # sticker_id = message["sticker"]["id"]
        message_body = "sticker messages not yet supported"
    response = "you said: " + message_body
    send_whatsapp_message(body, response)


# handle audio messages
def handle_audio_message(audio_id):
    """handle audio messages"""
    audio_url = get_media_url(audio_id)
    audio_bytes = download_media_file(audio_url)
    audio_data = convert_audio_bytes(audio_bytes)
    audio_text = recognize_audio(audio_data)
    message = (
        "Please summarize the following message in its original language "
        f"as a list of bullet-points: {audio_text}"
    )
    return message


# get the media url from the media id
def get_media_url(media_id):
    """get the media url from the media id"""
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers, timeout=30)
    log.info("media id response: {%s}", response.json())
    return response.json()["url"]


# download the media file from the media url
def download_media_file(media_url):
    """download the media file from the media url"""
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    response = requests.get(media_url, headers=headers, timeout=30)
    log.info("first 10 digits of the media file: {%s}", response.content[:10])
    return response.content


# convert ogg audio bytes to audio data which speechrecognition library can process
def convert_audio_bytes(audio_bytes):
    """convert ogg audio bytes to audio data which speechrecognition library can process"""
    ogg_audio = pydub.AudioSegment.from_ogg(io.BytesIO(audio_bytes))
    ogg_audio = ogg_audio.set_sample_width(4)
    wav_bytes = ogg_audio.export(format="wav").read()
    audio_data, sample_rate = sf.read(io.BytesIO(wav_bytes), dtype="int32")
    sample_width = audio_data.dtype.itemsize
    log.info("audio sample_rate:{%s}, sample_width:{%s}", sample_rate, sample_width)
    audio = sr.AudioData(audio_data, sample_rate, sample_width)
    return audio


# language for speech to text recognition
# pylint: disable=W0511
# TODO: detect this automatically based on the user's language
LANGUAGE = "en-US"


# run speech recognition on the audio data
def recognize_audio(audio_bytes):
    """run speech recognition on the audio data"""
    recognizer = sr.Recognizer()
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUAGE)
    return audio_text


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    """send the response as a WhatsApp message back to the user"""
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
    }
    url = "https://graph.facebook.com/v15.0/" + phone_number_id + "/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(url, json=data, headers=headers, timeout=30)
    log.info("whatsapp message response: {%s}", response)
    response.raise_for_status()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(debug=True, host="0.0.0.0", port=port)
