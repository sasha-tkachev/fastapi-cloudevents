import json
from typing import Any, Type

from cloudevents.conversion import to_dict, to_json
from cloudevents.http import CloudEvent, from_http
from starlette.requests import Request

from fastapi_cloudevents.content_type import is_json_content_type_event
from fastapi_cloudevents.settings import CloudEventSettings


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
    _json: Any
    _body: Any
    
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            event = _best_effort_fix_json_data_payload(
                from_http(dict(self.headers), body)
            )
            self._json = to_dict(event)
            self._body = to_json(event)
        return self._body

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["CloudEventRequest"]:
        class ConfiguredCloudEventRequest(cls):
            _settings = settings

        return ConfiguredCloudEventRequest
