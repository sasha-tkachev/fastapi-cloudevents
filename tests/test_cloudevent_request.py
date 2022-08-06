import pytest
from cloudevents.http import CloudEvent

from fastapi_cloudevents.cloudevent_request import (
    _is_json_content_type,
    _should_fix_json_data_payload,
)


@pytest.mark.parametrize(
    "given, expected",
    [
        (None, True),
        ("application/json", True),
        ("application/xml", False),
        ("json", False),
        ("plain/text", False),
        ("plain/json", True),
        ("application/something+json", True),
        ("application/cloudevents+json", True),
        ("dummy/json", True),
        ("dummy/dummy+json", True),
        ("plain/dummy+json", True),
        ("/dummy+json", True),
        ("dummy/+json", True),
        ("/+json", True),
        ("/json", True),
    ],
)
def test_is_json_content_type_matches_golden_samples(given, expected):
    assert _is_json_content_type(given) == expected


@pytest.mark.parametrize(
    "given, expected",
    [
        (CloudEvent(attributes={"source": "a", "type": "a"}, data="{}"), True),
        (
            CloudEvent(
                attributes={
                    "source": "a",
                    "type": "a",
                    "datacontenttype": "application/json",
                },
                data="{}",
            ),
            True,
        ),
        (
            CloudEvent(
                attributes={
                    "source": "a",
                    "type": "a",
                    "datacontenttype": "plain/text",
                },
                data="{}",
            ),
            False,
        ),
        (
            CloudEvent(
                attributes={
                    "source": "a",
                    "type": "a",
                    "datacontenttype": "application/json",
                },
                data={},
            ),
            False,
        ),
        (
            CloudEvent(
                attributes={
                    "source": "a",
                    "type": "a",
                    "datacontenttype": "plain/text",
                },
                data={},
            ),
            False,
        ),
    ],
)
def test_should_fix_payload_matches_golden_sample(given, expected):
    assert _should_fix_json_data_payload(given) == expected
