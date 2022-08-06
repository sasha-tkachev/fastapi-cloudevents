import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.pydantic import CloudEvent, from_http
from starlette.testclient import TestClient

from examples.events_and_basemodels_mixed.example_server import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_event_response_should_be_a_cloudevent(client):
    response = client.post("/event-response", data='{"my_value": "Hello World"}')
    assert from_http(headers=response.headers, data=response.content).data == {
        "my_value": "Hello World"
    }


def test_model_response_should_be_a_simple_model(client):
    response = client.post("/event-response", data='{"my_value": "Hello World"}')
    assert response.json() == {"my_value": "Hello World"}
