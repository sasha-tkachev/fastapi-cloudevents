from typing import Callable, Type

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cloudevents.cloudevent_request import CloudEventRequest
from fastapi_cloudevents.cloudevent_response import _CloudEventResponse
from fastapi_cloudevents.settings import CloudEventSettings


def _route_source(request: Request, settings: CloudEventSettings):
    if settings.default_source:
        return settings.default_source
    return str(request.url)


class CloudEventRoute(APIRoute):
    _settings: CloudEventSettings = CloudEventSettings()
    _request_class: Type[CloudEventRequest] = CloudEventRequest

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(
                self._request_class(request.scope, request.receive)
            )
            if isinstance(response, _CloudEventResponse):
                response.replace_default_source(
                    new_source=_route_source(request, self._settings)
                )
            return response

        return custom_route_handler

    @classmethod
    def configured(cls, settings: CloudEventSettings) -> Type["CloudEventRoute"]:
        class ConfiguredCloudEventRoute(cls):
            _settings: CloudEventSettings = settings
            _request_class = CloudEventRequest.configured(settings)

        return ConfiguredCloudEventRoute
