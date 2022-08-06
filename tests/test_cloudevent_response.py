import json
from typing import AnyStr, Dict

import pytest

from fastapi_cloudevents import StructuredCloudEventResponse
from fastapi_cloudevents.cloudevent import DEFAULT_SOURCE
from fastapi_cloudevents.cloudevent_response import (RawHeaders,
                                                     _encoded_string,
                                                     _update_headers)


def test_bytes_is_already_encoded():
    v = b"Hello World"
    assert _encoded_string(v) is v


def test_str_should_be_encoded_in_utf_8():
    assert _encoded_string("Hello World") == b"Hello World"


@pytest.mark.parametrize(
    "given_headers, new_headers, expected",
    [
        (
            [(b"ce-source", b"my-source"), (b"content-type", b"application/json")],
            {"ce-source": "your-source"},
            [(b"ce-source", b"your-source"), (b"content-type", b"application/json")],
        ),
        (
            [(b"ce-source", b"my-source"), (b"content-type", b"application/json")],
            {"Content-Type": b"plain/text"},
            [(b"ce-source", b"my-source"), (b"content-type", b"plain/text")],
        ),
    ],
)
def test_update_headers_match_golden_sample(
    given_headers: RawHeaders, new_headers: Dict[AnyStr, AnyStr], expected: RawHeaders
):
    result = _update_headers(given_headers, new_headers)
    assert set(result) == set(expected)


def test_re_rendering_structured_response_should_update_content_length():
    response = StructuredCloudEventResponse({"a": "b"})
    old_content_length = dict(response.raw_headers)[b"content-length"]
    response._re_render({"a": "b", "c": "d"})
    assert dict(response.raw_headers)[b"content-length"] != old_content_length


@pytest.mark.parametrize(
    "given, expected_body, expected_headers",
    [
        pytest.param(
            StructuredCloudEventResponse({"source": "non-default-source"}),
            {"source": "non-default-source"},
            [
                (b"content-length", b"31"),
                (b"content-type", b"application/cloudevents+json"),
            ],
            id="non default source must not be replaced",
        ),
        pytest.param(
            StructuredCloudEventResponse({"source": DEFAULT_SOURCE}),
            {"source": "new-source"},
            [
                (b"content-length", b"23"),
                (b"content-type", b"application/cloudevents+json"),
            ],
            id="default source should be replaced",
        ),
        pytest.param(
            StructuredCloudEventResponse(
                {"source": "dummy" + DEFAULT_SOURCE + "another"}
            ),
            {"source": "dummyfastapianother"},
            [
                (b"content-length", b"32"),
                (b"content-type", b"application/cloudevents+json"),
            ],
            id=(
                "sources which contain the default source as a sub string must not be "
                "affected"
            ),
        ),
    ],
)
def test_structured_replace_default_source_matches_golden_sample(
    given: StructuredCloudEventResponse,
    expected_body: Dict[str, str],
    expected_headers: RawHeaders,
):
    given.replace_default_source("new-source")
    assert json.loads(given.body) == expected_body
    assert set(given.raw_headers) == set(expected_headers)
