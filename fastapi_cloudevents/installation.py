import logging
from typing import Optional, Type

from fastapi import FastAPI
from starlette.responses import JSONResponse

from fastapi_cloudevents import (BinaryCloudEventResponse,
                                 StructuredCloudEventResponse)
from fastapi_cloudevents.cloudevent_response import _CloudEventResponse
from fastapi_cloudevents.cloudevent_route import CloudEventRoute
from fastapi_cloudevents.settings import CloudEventSettings, ResponseMode


def _choose_default_response_class(
    settings: CloudEventSettings,
) -> Type[_CloudEventResponse]:
    if settings.default_response_mode == ResponseMode.binary:
        return BinaryCloudEventResponse.configured(settings)
    if settings.default_response_mode == ResponseMode.structured:
        return StructuredCloudEventResponse.configured(settings)
    raise ValueError("Unknown response mode {}".format(settings.default_response_mode))


def install_fastapi_cloudevents(
    app: FastAPI,
    settings: Optional[CloudEventSettings] = None,
) -> FastAPI:
    if settings is None:
        settings = CloudEventSettings()
    if app.default_response_class == JSONResponse:
        app.default_response_class = _choose_default_response_class(settings)
    else:
        logging.warning(
            "app default response class was not json response, "
            "cannot override to binary CloudEvent response, this may "
            "cause issues"
        )
    app.router.route_class = CloudEventRoute.configured(settings)
    return app
