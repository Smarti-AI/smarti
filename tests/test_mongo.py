"""test mongo layer"""

import smarti.storage.mongo_client as mc


def test_read_workbooks(mongo_client):
    """handle whatsapp message"""
    assert len(mc.read_workbooks(mongo_client, "id")) == 2