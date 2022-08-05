from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cloudevents.cloudevent_request import CloudEventRequest


class CloudEventRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = CloudEventRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
