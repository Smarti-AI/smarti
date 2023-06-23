"""test logic"""

import smarti.logic.facade as pf


def test_index(flask_app, client):
    """test flask_app default"""
    assert flask_app is not None
    res = client.get("/")
    assert res.status_code == 200
    content = res.get_data(as_text=True)
    assert "Smarti" in content


def test_heroku_boot():
    """test content of boot file"""
    with open("./Procfile", mode="r", encoding="utf-8") as proc_file:
        line = proc_file.readlines()[0]
        assert line.split(" ")[-1] == "smarti.app:app"


def test_upload_workbook():
    """test workbook upload"""
    body = b""
    assert pf.upload_workbook(body) == 0


def test_send_message():
    """test chat"""
    assert pf.send_message("") == ""
