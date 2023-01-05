import pytest
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_cloudevents import CloudEventSettings, install_fastapi_cloudevents
from fastapi_cloudevents.installation import _choose_default_response_class


def test_user_warned_when_overriding_default_response_object(caplog):
    app = FastAPI(default_response_class=ORJSONResponse)
    install_fastapi_cloudevents(app)
    assert "WARNING" in caplog.text


def test_choose_default_response_class_invalid_option_must_fail():
    settings = CloudEventSettings()
    settings.default_response_mode = object()
    with pytest.raises(ValueError):
        _choose_default_response_class(settings)
