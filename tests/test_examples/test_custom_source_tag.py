import json

import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent, from_http
from starlette.testclient import TestClient

from examples.custom_source_tag.example_server import app


@pytest.fixture()
def client():
    return TestClient(app)


_DUMMY_SOURCE = "our-source"
_DUMMY_TYPE = "my.event.v1"
_DUMMY_JSON_DATA = {"a": "b"}
_EXPECTED_HEADERS = {
    "content-length",
    "content-type",
    "ce-specversion",
    "ce-id",
    "ce-source",
    "ce-type",
    "ce-time",
}
_EXPECTED_RESPONSE_HEADER_VALUES = {
    "content-length": str(len(json.dumps(_DUMMY_JSON_DATA))),
    "content-type": "application/json",
    "ce-specversion": "1.0",
    "ce-source": "http://testserver/",
    "ce-type": "my.response-type.v1",
}


def test_binary_request_is_in_binary_format(client):
    headers, data = to_binary(
        CloudEvent({"type": _DUMMY_TYPE, "source": _DUMMY_SOURCE}, _DUMMY_JSON_DATA)
    )
    for i in range(10):  # example server has random element
        response = client.post("/", headers=headers, data=data)
        assert response.status_code == 200
        event = from_http(response.headers, response.content)
        assert event.get("source") in ("my-source", "his-source")
