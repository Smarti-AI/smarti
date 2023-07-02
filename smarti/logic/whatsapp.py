"""whatsapp.py - handle WhatsApp messages"""
import logging
import os
import sys

import requests
from flask import jsonify

# smarti imports
from smarti.logic import sound, db
from smarti.logic.bot import onboarding

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


def get_whatsapp_verify_token():
    """get the WhatsApp verify token from the environment variables"""
    return os.environ.get("WHATSAPP_VERIFY_TOKEN")


def get_whatsapp_token():
    """get the WhatsApp token from the environment variables"""
    return os.environ.get("WHATSAPP_ACCESS_TOKEN")


# Required webhook verification for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(req, verify_token):
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
    message_body = parse_message(body)
    log.info("received message: {%s}", message_body)

    # db.save_new_user_message(message_body)
    messages = db.load_messages()
    response = onboarding.get_next_message(messages, message_body)
    db.save_new_bot_message(response)
    send_whatsapp_message(body, response)


def parse_message(body):
    """parse WhatsApp message"""
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
    return message_body


# handle audio messages
def handle_audio_message(audio_id):
    """handle audio messages"""
    audio_url = get_media_url(audio_id)
    audio_bytes = download_media_file(audio_url)
    audio_data = sound.convert_audio_bytes(audio_bytes)
    audio_text = sound.recognize_audio(audio_data)
    return audio_text


# get the media url from the media id
def get_media_url(media_id):
    """get the media url from the media id"""
    headers = {
        "Authorization": f"Bearer {get_whatsapp_token()}",
    }
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers, timeout=30)
    log.info("media id response: {%s}", response.json())
    return response.json()["url"]


# download the media file from the media url
def download_media_file(media_url):
    """download the media file from the media url"""
    headers = {
        "Authorization": f"Bearer {get_whatsapp_token()}",
    }
    response = requests.get(media_url, headers=headers, timeout=30)
    log.info("first 10 digits of the media file: {%s}", response.content[:10])
    return response.content


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    """send the response as a WhatsApp message back to the user"""
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    headers = {
        "Authorization": f"Bearer {get_whatsapp_token()}",
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
