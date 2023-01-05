import pytest
from cloudevents.conversion import to_binary, to_structured
from cloudevents.pydantic import CloudEvent, from_http
from starlette.testclient import TestClient
import sys

if sys.version_info[1] >= 8:
    from examples.type_routing.example_server import app

    @pytest.fixture()
    def client():
        return TestClient(app)

    @pytest.mark.parametrize(
        "given_type, expected_type",
        [
            ("my.type.v1", "my.response-type.v1"),
            ("your.type.v1", "your.response-type.v1"),
        ],
    )
    @pytest.mark.parametrize("to_http", (to_binary, to_structured))
    def test_binary_request_is_in_binary_format(
        client, to_http, given_type, expected_type
    ):
        headers, data = to_http(CloudEvent(type=given_type, source="dummy-source"))
        response = client.post("/", headers=headers, data=data)
        assert (
            from_http(headers=response.headers, data=response.content).type
            == expected_type
        )
