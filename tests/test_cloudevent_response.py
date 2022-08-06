from typing import AnyStr, Dict

import pytest

from fastapi_cloudevents.cloudevent_response import (
    RawHeaders,
    _encoded_string,
    _update_headers,
)


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
    for value in expected:  # we cannot test order
        assert value in result
