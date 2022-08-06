import logging
from typing import Optional, Type

from fastapi import FastAPI
from starlette.responses import JSONResponse

from fastapi_cloudevents import BinaryCloudEventResponse
from fastapi_cloudevents.cloudevent_response import _CloudEventResponse
from fastapi_cloudevents.cloudevent_route import CloudEventRoute
from fastapi_cloudevents.settings import CloudEventSettings


def install_fastapi_cloudevents(
    app: FastAPI,
    settings: Optional[CloudEventSettings] = None,
    default_response_class: Optional[Type[_CloudEventResponse]] = None,
) -> FastAPI:
    if settings is None:
        settings = CloudEventSettings()
    if default_response_class is None:
        if app.default_response_class == JSONResponse:
            default_response_class = BinaryCloudEventResponse
        else:
            logging.warning(
                "app default response class was not json response, "
                "cannot override to binary CloudEvent response, this may "
                "cause issues"
            )
            default_response_class = app.default_response_class
    app.default_response_class = default_response_class
    app.router.route_class = CloudEventRoute.configured(settings)
    return app

