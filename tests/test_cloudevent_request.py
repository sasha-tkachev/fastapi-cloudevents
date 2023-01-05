from typing import AsyncGenerator

import pytest
from cloudevents.exceptions import MissingRequiredFields
from cloudevents.http import CloudEvent

from fastapi_cloudevents import CloudEventRequest, CloudEventSettings
from fastapi_cloudevents.cloudevent_request import (
    _best_effort_fix_json_data_payload,
    _should_fix_json_data_payload,
)


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


def test_best_effort_event_fixing_should_not_fail_on_invalid_json():
    corrupt_json = "{"
    assert (
        _best_effort_fix_json_data_payload(
            CloudEvent(attributes={"source": "a", "type": "a"}, data=corrupt_json)
        ).data
        == corrupt_json
    )


def test_best_effort_event_fixing_should_fix_valid_json():
    assert _best_effort_fix_json_data_payload(
        CloudEvent(attributes={"source": "a", "type": "a"}, data='{"hello": "world"}')
    ).data == {"hello": "world"}


class FakeInvalidCloudEventRequest(CloudEventRequest):
    def __init__(self):
        super(FakeInvalidCloudEventRequest, self).__init__(
            {"type": "http", "headers": []}
        )

    async def stream(self) -> AsyncGenerator[bytes, None]:
        yield b'{"a": "b"}'


@pytest.mark.asyncio
async def test_when_disallowed_body_access_of_invalid_cloudevent_request_must_fail():
    with pytest.raises(MissingRequiredFields):
        await FakeInvalidCloudEventRequest.configured(
            CloudEventSettings(allow_non_cloudevent_models=False)
        )().body()
