import json

import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent, from_http
from starlette.testclient import TestClient

from examples.custom_source_tag.example_server import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_binary_request_is_in_binary_format(client):
    for i in range(10):  # example server has random element
        response = client.get("/")
        assert response.status_code == 200
        event = from_http(response.headers, response.content)
        assert event.get("source") in ("my-source", "his-source")
