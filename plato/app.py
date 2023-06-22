"""flask app runner"""

import os
import sys
import logging
import requests
from flask import Flask, jsonify, request


app = Flask(__name__, static_url_path="/static")
log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


# Access token for your WhatsApp business account app
whatsapp_token = os.environ.get("WHATSAPP_TOKEN", "EAALABLp6AXUBANXmeoyMt9lF5z28Qn7iFxLFEMuFZCPqcgxHbRvybY9VSzuapiUttn2C1DZBFr0S4n9NWnXfXoKmtUIkHgv1hGfsncVHkuyRLJJan7qvOcQZC6a8CJQCiZBG6ZCeVAFaKFKZCHiCCVjq2S9n7ec7LYSwb0FMZCrQ0ta5dvEIBr5ko5VSWdaScZB1jUZAlDHNLygZDZD")

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
    """ " Parse Request body in json format"""
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
        # audio_id = message["audio"]["id"]
        message_body = "voice messages not yet supported"
    response = "you said: " + message_body
    send_whatsapp_message(body, response)


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
