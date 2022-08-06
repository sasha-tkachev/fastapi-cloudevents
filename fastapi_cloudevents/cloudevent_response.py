import json
import typing
from abc import abstractmethod

from cloudevents.abstract import AnyCloudEvent
from cloudevents.conversion import to_binary
from cloudevents.http import from_dict
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from fastapi_cloudevents.cloudevent import DEFAULT_SOURCE


class _CloudEventResponse(JSONResponse):
    @abstractmethod
    def replace_default_source(self, new_source: str):
        pass


class StructuredCloudEventResponse(_CloudEventResponse):
    """
    Nothing to implement because structured CloudEvents are literally json objects
    """

    @abstractmethod
    def replace_default_source(self, new_source: str):
        result = json.loads(self.body)
        result["source"] = result["source"].replace(DEFAULT_SOURCE, new_source)
        self.body = self.render(result)
        content_length = str(len(self.body))
        headers = dict(self.raw_headers)
        headers[b"content-length"] = content_length.encode("latin-1")
        self.raw_headers = list(headers.items())


class BinaryCloudEventResponse(_CloudEventResponse):
    def __init__(
        self,
        content: typing.Optional[AnyCloudEvent] = None,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        super(BinaryCloudEventResponse, self).__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
        self.raw_headers = self._render_headers(content, headers=self.raw_headers)

    def render(self, content: typing.Optional[typing.Any]) -> bytes:
        if content is None:
            return b""
        _, body = to_binary(from_dict(content))
        return body

    @classmethod
    def _render_headers(cls, content: typing.Optional[typing.Any], headers):
        if content is None:
            return headers
        ce_headers, _ = to_binary(from_dict(content))
        ce_headers = [
            (k.encode("utf-8"), v.encode("utf-8")) for k, v in ce_headers.items()
        ]
        result = dict(headers)
        result.update(ce_headers)
        return list(result.items())

    @abstractmethod
    def replace_default_source(self, new_source: str):
        result = dict(self.raw_headers)
        source = result.get(b"ce-source", b"").decode("utf-8")
        source = source.replace(DEFAULT_SOURCE, new_source)
        result[b"ce-source"] = source.encode("utf-8")
        self.raw_headers = list(result.items())
