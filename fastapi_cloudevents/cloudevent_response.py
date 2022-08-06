import json
import typing
from abc import abstractmethod
from typing import Any, AnyStr, Dict, List, Optional, Union

from cloudevents.abstract import AnyCloudEvent
from cloudevents.conversion import to_binary
from cloudevents.http import from_dict
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response

from fastapi_cloudevents.cloudevent import DEFAULT_SOURCE, DEFAULT_SOURCE_ENCODED


class _CloudEventResponse:
    @abstractmethod
    def replace_default_source(self, new_source: str):
        pass


RawHeaders = List[Union[bytes, Any]]


def _encoded_string(s: AnyStr) -> bytes:
    if isinstance(s, bytes):
        return s
    return s.encode("utf-8")


def _update_headers(
    headers: RawHeaders, new_headers: Dict[AnyStr, AnyStr]
) -> RawHeaders:
    headers = dict(headers)
    headers.update(
        {_encoded_string(k).lower(): _encoded_string(v) for k, v in new_headers.items()}
    )
    return list(headers.items())


class StructuredCloudEventResponse(JSONResponse, _CloudEventResponse):
    """
    Nothing to implement because structured CloudEvents are literally json objects
    """

    # starlette response does not init it in __init__ directly, so we need to hint it
    raw_headers: RawHeaders

    # https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md#3-envelope
    media_type = "application/cloudevents+json"

    @abstractmethod
    def replace_default_source(self, new_source: str):
        result = json.loads(self.body)
        if result.get("source") == DEFAULT_SOURCE:
            result["source"] = new_source
        self._re_render(result)

    def _re_render(self, content: typing.Any) -> None:
        self.body = self.render(content)
        content_length = str(len(self.body))
        self.raw_headers = _update_headers(
            self.raw_headers, {b"content-length": content_length.encode("latin-1")}
        )


_CE_SOURCE_HEADER_NAME = b"ce-source"


class BinaryCloudEventResponse(Response, _CloudEventResponse):
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
    def _render_headers(cls, content: typing.Optional[typing.Any], headers: RawHeaders):
        if content is None:
            return headers
        ce_headers, _ = to_binary(from_dict(content))
        headers = _update_headers(headers, ce_headers)
        return headers

    @abstractmethod
    def replace_default_source(self, new_source: str):
        if (_CE_SOURCE_HEADER_NAME, DEFAULT_SOURCE_ENCODED) in self.raw_headers:
            self.raw_headers = _update_headers(
                self.raw_headers, {_CE_SOURCE_HEADER_NAME: new_source.encode("utf-8")}
            )
