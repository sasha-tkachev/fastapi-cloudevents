import json
import re

from cloudevents.conversion import to_dict, to_json
from cloudevents.http import from_http
from starlette.requests import Request

_JSON_CONTENT_TYPE = re.compile(r"^.+?/.*\+?json$", flags=re.IGNORECASE)


class CloudEventRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "ce-specversion" in self.headers:
                event = from_http(dict(self.headers), body)
                if isinstance(event.data, (str, bytes)):
                    datacontenttype = event.get("datacontenttype")
                    if datacontenttype is None or _JSON_CONTENT_TYPE.match(
                        datacontenttype
                    ):
                        try:
                            event.data = json.loads(event.data)
                        except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
                            pass
                body = to_json(event)
                self._json = to_dict(event)
            self._body = body
        return self._body
