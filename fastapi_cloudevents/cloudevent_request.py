import json
import re

from cloudevents.conversion import to_dict, to_json
from cloudevents.http import CloudEvent, from_http
from starlette.requests import Request

_JSON_CONTENT_TYPE = re.compile(r"^.+?/.*\+?json$", flags=re.IGNORECASE)


def _should_fix_json_data_payload(event: CloudEvent):
    if isinstance(event.data, (str, bytes)):
        data_content_type = event.get("datacontenttype")
        return data_content_type is None or _JSON_CONTENT_TYPE.match(data_content_type)
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
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "ce-specversion" in self.headers:
                event = from_http(dict(self.headers), body)
                event = _best_effort_fix_json_data_payload(event)
                body = to_json(event)
                self._json = to_dict(event)
            self._body = body
        return self._body
