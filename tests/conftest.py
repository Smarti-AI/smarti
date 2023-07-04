"""conftest"""

import os
import pytest
import mongomock
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


@pytest.fixture
def input_folder():
    """file containing formula"""
    path = os.path.abspath(__file__)
    dir_name = os.path.dirname(path)
    return f"{dir_name}/input/"


@pytest.fixture
def mongo_client():
    """mongo client"""
    env = {"MONGO_CONN": "url"}
    return mongomock.MongoClient(env.get("MONGO_CONN", ""))
