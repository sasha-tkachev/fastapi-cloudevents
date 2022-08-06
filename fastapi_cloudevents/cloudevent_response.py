import typing

from cloudevents.abstract import AnyCloudEvent
from cloudevents.conversion import to_binary
from cloudevents.http import from_dict
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


class _CloudEventResponse(JSONResponse):
    pass


class StructuredCloudEventResponse(_CloudEventResponse):
    """
    Nothing to implement because structured CloudEvents are literally json objects
    """
    pass


class BinaryCloudEventResponse(StructuredCloudEventResponse):
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

