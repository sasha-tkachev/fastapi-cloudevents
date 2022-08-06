import json
import typing
from abc import abstractmethod
from typing import Any, AnyStr, Dict, List, Type, Union

from cloudevents.abstract import CloudEvent
from cloudevents.conversion import to_binary
from cloudevents.http import from_dict
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response

from fastapi_cloudevents.settings import CloudEventSettings
from fastapi_cloudevents.cloudevent import (DEFAULT_SOURCE,
                                            DEFAULT_SOURCE_ENCODED)
from fastapi_cloudevents.content_type import is_json_content_type_event


class _CloudEventResponse:
    @abstractmethod
    def replace_default_source(self, new_source: str):
        pass  # pragma: no cover


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

    _settings: CloudEventSettings = CloudEventSettings()

    # starlette response does not init it in __init__ directly, so we need to hint it
    raw_headers: RawHeaders

    # https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md#3-envelope
    media_type = "application/cloudevents+json"

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

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["_CloudEventResponse"]:
        class ConfiguredStructuredCloudEventResponse(cls):
            _settings = settings

        return ConfiguredStructuredCloudEventResponse


_CE_SOURCE_HEADER_NAME = b"ce-source"


def _empty_body_value(event: CloudEvent):
    """
    We MUST return a non-None http payload to the client, but the to_binary
    function returned None.
    The sensible thing to do is to return b"" an empty buffer.
    The problem is that if the datacontenttype of the event
    is `application/json` (which it is by default for CloudEvents) b"" is an invalid
    json buffer, and trying to parse it on the client will result in an error. So to
    handle this case We return b"null" so when the client
    parses the body he will get a `None`
    """
    if is_json_content_type_event(event):
        return b"null"  # empty buffer is not a valid json value
    else:
        return b""


class BinaryCloudEventResponse(Response, _CloudEventResponse):
    _settings: CloudEventSettings = CloudEventSettings()

    def __init__(
        self,
        content: Dict[AnyStr, Any],
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        super(BinaryCloudEventResponse, self).__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="application/json" if media_type is None else media_type,
            # the default content type is json, but may be overridden by the event
            # datacontenttype attribute
            background=background,
        )
        self.raw_headers = self._render_headers(content, headers=self.raw_headers)

    def render(self, content: Dict[AnyStr, Any]) -> bytes:
        event = from_dict(content)
        _, body = to_binary(event)
        if body is None:
            return _empty_body_value(event)
        return body

    @classmethod
    def _render_headers(cls, content: Dict[AnyStr, Any], headers: RawHeaders):
        ce_headers, _ = to_binary(from_dict(content))
        headers = _update_headers(headers, ce_headers)
        return headers

    def replace_default_source(self, new_source: str):
        if (_CE_SOURCE_HEADER_NAME, DEFAULT_SOURCE_ENCODED) in self.raw_headers:
            self.raw_headers = _update_headers(
                self.raw_headers, {_CE_SOURCE_HEADER_NAME: new_source.encode("utf-8")}
            )

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["_CloudEventResponse"]:
        class ConfiguredBinaryCloudEventResponse(cls):
            _settings = settings

        return ConfiguredBinaryCloudEventResponse
