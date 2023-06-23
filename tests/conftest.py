"""conftest"""

import pytest
import smarti.app


@pytest.fixture
def flask_app():
    """return flask app"""
    yield smarti.app.app


@pytest.fixture
def client(flask_app):
    """test client"""
    return flask_app.test_client()
