import json

from cloudevents.exceptions import MissingRequiredFields
from typing import AnyStr, Dict

import pytest

from fastapi_cloudevents import (
    BinaryCloudEventResponse,
    StructuredCloudEventResponse,
    CloudEventSettings,
)
from fastapi_cloudevents.cloudevent import DEFAULT_SOURCE
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


@pytest.mark.parametrize(
    "given, expected_headers",
    [
        pytest.param(
            BinaryCloudEventResponse(
                {
                    "source": "non-default-source",
                    "type": "dummy",
                    "id": "1",
                    "time": "1",
                }
            ),
            [
                (b"ce-id", b"1"),
                (b"ce-source", b"non-default-source"),
                (b"ce-specversion", b"1.0"),
                (b"ce-time", b"1"),
                (b"ce-type", b"dummy"),
                (b"content-type", b"application/json"),
                (b"content-length", b"4"),
            ],
            id="non default source must not be replaced",
        ),
        pytest.param(
            BinaryCloudEventResponse(
                {"source": DEFAULT_SOURCE, "type": "dummy", "id": "1", "time": "1"}
            ),
            [
                (b"ce-id", b"1"),
                (b"ce-source", b"new-source"),
                (b"ce-specversion", b"1.0"),
                (b"ce-time", b"1"),
                (b"ce-type", b"dummy"),
                (b"content-type", b"application/json"),
                (b"content-length", b"4"),
            ],
            id="default source should be replaced",
        ),
        pytest.param(
            BinaryCloudEventResponse(
                {
                    "source": "dummy" + DEFAULT_SOURCE + "another",
                    "type": "dummy",
                    "id": "1",
                    "time": "1",
                }
            ),
            [
                (b"ce-id", b"1"),
                (b"ce-source", b"dummyfastapianother"),
                (b"ce-specversion", b"1.0"),
                (b"ce-time", b"1"),
                (b"ce-type", b"dummy"),
                (b"content-type", b"application/json"),
                (b"content-length", b"4"),
            ],
            id=(
                "sources which contain the default source as a sub string must not be "
                "affected"
            ),
        ),
    ],
)
def test_binary_replace_default_source_matches_golden_sample(
    given: BinaryCloudEventResponse,
    expected_headers: RawHeaders,
):
    given.replace_default_source("new-source")
    assert set(given.raw_headers) == set(expected_headers)


@pytest.mark.parametrize(
    "content_type, expected_value",
    [
        (None, b"null"),
        ("plain/text", b""),
        ("application/json", b"null"),
        ("dummy/dummy+json", b"null"),
    ],
)
def test_binary_response_given_empty_data_return_golden_empty_value(
    content_type, expected_value
):
    assert (
        BinaryCloudEventResponse(
            {
                "source": "dummy",
                "type": "dummy",
                "data": None,
                "datacontenttype": content_type,
            }
        ).body
        == expected_value
    )


_INVALID_CLOUDEVENT_CONTENT = {"a": "b"}


def test_when_allowed_rendering_invalid_cloudevent_binary_response_must_rendered_to_json():
    CloudEventSettings(allow_non_cloudevent_models=True)
    assert (
        json.loads(
            BinaryCloudEventResponse.configured(
                CloudEventSettings(allow_non_cloudevent_models=True)
            )({}).render(_INVALID_CLOUDEVENT_CONTENT)
        )
        == _INVALID_CLOUDEVENT_CONTENT
    )


def test_when_disallowed_rendering_invalid_cloudevent_binary_response_must_fail():
    with pytest.raises(MissingRequiredFields):
        BinaryCloudEventResponse.configured(
            CloudEventSettings(allow_non_cloudevent_models=False)
        )({}).render(_INVALID_CLOUDEVENT_CONTENT)


def test_when_disallowed_rendering_invalid_cloudevent_binary_headers_must_fail():
    with pytest.raises(MissingRequiredFields):
        BinaryCloudEventResponse.configured(
            CloudEventSettings(allow_non_cloudevent_models=False)
        )._render_headers(_INVALID_CLOUDEVENT_CONTENT, [])
