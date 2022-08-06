from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cloudevents.cloudevent_request import CloudEventRequest
from fastapi_cloudevents.cloudevent_response import _CloudEventResponse
import re

_CE_SOURCE_TAG_PREFIX = re.compile(r"^ce-source:", flags=re.IGNORECASE)


def _is_source_tag(tag: str):
    return _CE_SOURCE_TAG_PREFIX.match(tag)


def _source_tag_to_source(source_tag: str) -> str:
    return _CE_SOURCE_TAG_PREFIX.sub("", source_tag)


def _route_source(route: APIRoute, request: Request) -> str:
    try:
        return next(map(_source_tag_to_source, filter(_is_source_tag, route.tags)))
    except StopIteration:
        return str(request.url)


class CloudEventRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(
                CloudEventRequest(request.scope, request.receive)
            )
            if isinstance(response, _CloudEventResponse):
                response.replace_default_source(new_source=_route_source(self, request))
            return response

        return custom_route_handler
