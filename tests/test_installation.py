from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_cloudevents import install_fastapi_cloudevents


def test_user_warned_when_overriding_default_response_object(caplog):
    app = FastAPI(default_response_class=ORJSONResponse)
    install_fastapi_cloudevents(app)
    assert "WARNING" in caplog.text
