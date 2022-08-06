from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cloudevents.cloudevent_request import CloudEventRequest
from fastapi_cloudevents.cloudevent_response import _CloudEventResponse


class CloudEventRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(
                CloudEventRequest(request.scope, request.receive)
            )
            if isinstance(response, _CloudEventResponse):
                response.replace_default_source(new_source=str(request.url))
            return response

        return custom_route_handler
