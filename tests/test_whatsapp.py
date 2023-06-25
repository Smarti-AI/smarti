"""test whatsapp"""


import smarti.app


def test_whatsapp_verify(request_context):
    """test flask_app default"""
    with request_context():
        req = type("", (object,), {"args": {}})()
        req.args["hub.mode"] = "subscribe"
        req.args["hub.verify_token"] = "token"
        req.args["hub.challenge"] = "challenge"
        res = smarti.app.verify(req, "token")
        assert res[1] == 200

        res = smarti.app.verify(req, "toke")
        assert res[1] == 403

        req.args["hub.mode"] = None
        res = smarti.app.verify(req, "toke")
        assert res[1] == 400


def test_whatsapp_handle_message(request_context, mocker):
    """test handle message"""
    with request_context():
        req = mocker.MagicMock()
        res = smarti.app.handle_message(req)
        assert res[1] == 500

        req.get_json.return_value = {}
        res = smarti.app.handle_message(req)
        assert res[1] == 404

        state = {"object": "a", "entry": [{"changes": [{"value": {}}]}]}

        req.get_json.return_value = state
        res = smarti.app.handle_message(req)
        assert res[1] == 200


def test_whatsapp_send_message(mocker):
    """test send message"""
    mock_request = mocker.patch("requests.post")

    value = {
        "value": {"metadata": {"phone_number_id": "+972"}, "messages": [{"from": "x"}]}
    }
    body = {"entry": [{"changes": [value]}]}
    smarti.app.send_whatsapp_message(body, "example message")
    assert mock_request.call_count == 1
