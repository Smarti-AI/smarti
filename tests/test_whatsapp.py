"""test whatsapp"""

import smarti.app


def test_whatsapp_verify(request_context):
    """test flask_app default"""
    with request_context():
        req = type("", (object,), {"args": {}})()
        req.args["hub.mode"] = "subscribe"
        req.args["hub.verify_token"] = "token"
        req.args["hub.challenge"] = "challenge"
        res = smarti.app.verify(req)
        assert not res is None
