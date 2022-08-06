import json
from typing import Type

from cloudevents.conversion import to_dict, to_json
from cloudevents.http import CloudEvent, from_http
from starlette.requests import Request

from fastapi_cloudevents import CloudEventSettings
from fastapi_cloudevents.content_type import is_json_content_type_event


def _should_fix_json_data_payload(event: CloudEvent):
    if isinstance(event.data, (str, bytes)):
        return is_json_content_type_event(event)
    else:
        return False  # not encoded json payload


def _best_effort_fix_json_data_payload(event: CloudEvent) -> CloudEvent:
    try:
        if _should_fix_json_data_payload(event):
            event.data = json.loads(event.data)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
        pass
    return event


class CloudEventRequest(Request):
    _settings: CloudEventSettings = CloudEventSettings()

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            event = from_http(dict(self.headers), body)
            event = _best_effort_fix_json_data_payload(event)
            body = to_json(event)
            self._json = to_dict(event)
            self._body = body
        return self._body

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["CloudEventRequest"]:
        class ConfiguredCloudEventRequest(CloudEventRequest):
            _settings = settings

        return ConfiguredCloudEventRequest
