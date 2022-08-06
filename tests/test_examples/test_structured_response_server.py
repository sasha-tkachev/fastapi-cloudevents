import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent
from starlette.testclient import TestClient

from examples.structured_response_server.example_server import app


@pytest.fixture()
def client():
    return TestClient(app)


_DUMMY_SOURCE = "my-source"
_DUMMY_TYPE = "my.event.v1"
_DUMMY_JSON_DATA = {"a": "b"}
_EXPECTED_KEYS = {
    "content-length",
    "content-type",
    "ce-specversion",
    "ce-id",
    "ce-source",
    "ce-type",
    "ce-time",
}
_EXPECTED_RESPONSE_HEADER_VALUES = {
    "specversion": "1.0",
    "source": "http://testserver/",
    "type": "com.my-corp.response.v1",
    "data": {"a": "b"},
}


@pytest.mark.parametrize("to_http", (to_binary, to_structured))
def test_structured_responses_should_contain_the_event_in_the_data(client, to_http):
    headers, data = to_http(
        CloudEvent({"type": _DUMMY_TYPE, "source": _DUMMY_SOURCE}, _DUMMY_JSON_DATA)
    )
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/cloudevents+json"

    assert {
        k: v
        for k, v in response.json().items()
        if k in _EXPECTED_RESPONSE_HEADER_VALUES
    } == _EXPECTED_RESPONSE_HEADER_VALUES
