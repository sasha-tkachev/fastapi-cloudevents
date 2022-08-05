import json
import re

from starlette.requests import Request

from cloudevents.pydantic import from_http

_JSON_CONTENT_TYPE = re.compile(r"^.+?/.*\+?json$", flags=re.IGNORECASE)


class CloudEventRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "ce-specversion" in self.headers:
                event = from_http(dict(self.headers), body)
                if isinstance(event.data, (str, bytes)):
                    if event.datacontenttype is None or _JSON_CONTENT_TYPE.match(
                            event.datacontenttype
                    ):
                        try:
                            event.data = json.loads(event.data)
                        except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
                            pass
                body = event.json()
            self._body = body
        return self._body