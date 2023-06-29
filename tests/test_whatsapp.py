"""test whatsapp"""
from speech_recognition import AudioData

from smarti.logic import whatsapp


def test_handle_whatsapp_message_text():
    """test handle whatsapp test message"""
    body = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "type": "text",
                                    "from": "123450",
                                    "text": {
                                        "body": "hello"
                                    }
                                }
                            ],
                            "metadata": {
                                "phone_number_id": "+972123456789"
                            }
                        }
                    }
                ]
            },
        ],
    }
    message = whatsapp.parse_message(body)
    assert message == "hello"


def test_handle_whatsapp_message_image():
    """test handle whatsapp image message"""
    body = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "type": "image",
                                    "from": "123450",
                                    "text": {
                                        "body": "hello"
                                    }
                                }
                            ],
                            "metadata": {
                                "phone_number_id": "+972123456789"
                            }
                        }
                    }
                ]
            },

        ],

    }

    message = whatsapp.parse_message(body)
    assert message == "image messages not yet supported"

def test_handle_whatsapp_message(mocker):
    """test handle whatsapp message"""
    parse_message = mocker.patch("smarti.logic.whatsapp.parse_message", return_value="hello")
    send_whatsapp_message = mocker.patch("smarti.logic.whatsapp.send_whatsapp_message", return_value="hello")
    whatsapp.handle_whatsapp_message("hello")
    assert parse_message.called
    assert send_whatsapp_message.called


def test_whatsapp_verify(request_context):
    """test flask_app default"""
    with request_context():
        req = type("", (object,), {"args": {}})()
        req.args["hub.mode"] = "subscribe"
        req.args["hub.verify_token"] = "token"
        req.args["hub.challenge"] = "challenge"
        res = whatsapp.verify(req, "token")
        assert res[1] == 200

        res = whatsapp.verify(req, "toke")
        assert res[1] == 403

        req.args["hub.mode"] = None
        res = whatsapp.verify(req, "toke")
        assert res[1] == 400


def test_whatsapp_handle_message(request_context, mocker):
    """test handle message"""
    with request_context():
        req = mocker.MagicMock()
        res = whatsapp.handle_message(req)
        assert res[1] == 500

        req.get_json.return_value = {}
        res = whatsapp.handle_message(req)
        assert res[1] == 404

        state = {"object": "a", "entry": [{"changes": [{"value": {}}]}]}

        req.get_json.return_value = state
        res = whatsapp.handle_message(req)
        assert res[1] == 200


def test_whatsapp_send_message(mocker):
    """test send message"""
    mock_request = mocker.patch("requests.post")

    value = {
        "value": {"metadata": {"phone_number_id": "+972"}, "messages": [{"from": "x"}]}
    }
    body = {"entry": [{"changes": [value]}]}
    whatsapp.send_whatsapp_message(body, "example message")
    assert mock_request.call_count == 1


def test_convert_audio_bytes():
    """test convert audio bytes"""
    with open('tests/hello_world.ogg', 'rb') as file:
        audio_bytes = file.read()
    audio_data = whatsapp.convert_audio_bytes(audio_bytes)
    assert isinstance(audio_data, AudioData)


def test_recognize_audio(mocker):
    """test recognize audio"""
    mocker.patch("speech_recognition.Recognizer.recognize_google", return_value="hello smarti")
    with open('tests/hello_world.ogg', 'rb') as file:
        audio_bytes = file.read()
    audio_data = whatsapp.convert_audio_bytes(audio_bytes)
    text = whatsapp.recognize_audio(audio_data)
    assert text == "hello smarti"


def test_download_media_file(mocker):
    """test download media file"""
    mock_request = mocker.patch("requests.get")
    mock_request.return_value.content = b"1234567890"
    audio_bytes = whatsapp.download_media_file("http://example.com/download/ogg")
    assert audio_bytes == b"1234567890"


def test_get_media_url(mocker):
    """test get media url"""
    mock_request = mocker.patch("requests.get")
    mock_request.return_value.json.return_value = {"url": "https://example.com/download/ogg"}
    url = whatsapp.get_media_url("123")
    assert url == "https://example.com/download/ogg"


def test_handle_audio_message(mocker):
    """test handle audio message"""
    mocker.patch("smarti.logic.whatsapp.get_media_url", return_value='tests/hello_world.ogg')

    with open('tests/hello_world.ogg', 'rb') as file:
        audio_bytes = file.read()

    mocker.patch("smarti.logic.whatsapp.download_media_file", return_value=audio_bytes)
    mocker.patch("speech_recognition.Recognizer.recognize_google", return_value="hello smarti")

    message = whatsapp.handle_audio_message("123")
    assert message == "hello smarti"
