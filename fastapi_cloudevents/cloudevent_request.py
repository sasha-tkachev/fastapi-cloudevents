import json
from typing import Type
from uuid import uuid4

from cloudevents.conversion import to_dict, to_json
from cloudevents.exceptions import MissingRequiredFields
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

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            headers = dict(self.headers)
            try:
                event = from_http(headers, body)
                event = _best_effort_fix_json_data_payload(event)
            except MissingRequiredFields:
                if self._settings.create_events_on_behalf_of_the_client:
                    event = CloudEvent(
                        {
                            "type": self._settings.default_user_event_type,
                            "source": uuid4().urn,  # we cannot identify this user
                            "datacontenttype": headers.get(b"content-type"),
                        },
                        data=body,
                    )
                else:
                    raise
            self._json = to_dict(event)
            self._body = to_json(event)
        return self._body

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["CloudEventRequest"]:
        class ConfiguredCloudEventRequest(cls):
            _settings = settings

        return ConfiguredCloudEventRequest
