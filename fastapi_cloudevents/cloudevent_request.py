import json
from typing import Optional, Type
from uuid import uuid4

from cloudevents.conversion import to_dict, to_json
from cloudevents.exceptions import MissingRequiredFields
from cloudevents.http import CloudEvent, from_http
from starlette.requests import Request, empty_receive, empty_send
from starlette.types import Receive, Scope, Send

from fastapi_cloudevents.content_type import is_json_content_type_event
from fastapi_cloudevents.settings import CloudEventSettings
from fastapi_cloudevents.source_tracking import SourceTracker


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

    def __init__(
        self, scope: Scope, receive: Receive = empty_receive, send: Send = empty_send,
            source_tracker: Optional[SourceTracker] = None
    ):
        super().__init__(scope=scope, receive=receive, send=send)
        if source_tracker is None:
            source_tracker = SourceTracker()
        self._source_tracker = source_tracker

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            headers = dict(self.headers)
            try:
                event = from_http(headers, body)
                event = _best_effort_fix_json_data_payload(event)
            except MissingRequiredFields:
                if self._settings.create_events_on_behalf_of_the_client:
                    source = self.cookies.get(self._settings.assigned_source_cookie_key)
                    if not source:
                        source = uuid4().urn  # we cannot identify this user
                        self._source_tracker.source_assigned_to_user = source

                    event = CloudEvent(
                        {
                            "type": self._settings.default_user_event_type,
                            "source": source,
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
