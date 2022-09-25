import json

import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent
from starlette.testclient import TestClient

from examples.simple_server.example_server import app


@pytest.fixture()
def client():
    return TestClient(app)


_DUMMY_SOURCE = "my-source"
_DUMMY_CONTENT_TYPE = "text/plain"
_DUMMY_TYPE = "my.event.v1"
_DUMMY_DATA = "Hello World"
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
    "content-length": str(len(json.dumps(_DUMMY_DATA))),
    "content-type": _DUMMY_CONTENT_TYPE,
    "ce-specversion": "1.0",
    "ce-source": "http://testserver/",
    "ce-type": "my.response-type.v1",
}


@pytest.mark.parametrize("to_http", (to_binary, to_structured))
def test_binary_request_is_in_binary_format(client, to_http):
    headers, data = to_http(
        CloudEvent({"type": _DUMMY_TYPE, "source": _DUMMY_SOURCE, "datacontenttype": _DUMMY_CONTENT_TYPE},
                   _DUMMY_DATA)
    )
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 200
    assert set(response.headers.keys()) == _EXPECTED_HEADERS
    assert {
        k: v
        for k, v in response.headers.items()
        if k in _EXPECTED_RESPONSE_HEADER_VALUES
    } == _EXPECTED_RESPONSE_HEADER_VALUES
    assert response.json() == _DUMMY_DATA
