"""conftest"""

import pytest
import smarti.app


@pytest.fixture(name="flask_app")
def fixture_app():
    """return flask app"""
    yield smarti.app.app


@pytest.fixture(name="request_context")
def fixture_request_context():
    """return flask app"""
    yield smarti.app.app.test_request_context


@pytest.fixture
def client(flask_app):
    """test client"""
    return flask_app.test_client()
