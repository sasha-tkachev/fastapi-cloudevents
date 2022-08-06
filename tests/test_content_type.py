import pytest

from fastapi_cloudevents.content_type import _is_json_content_type


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
