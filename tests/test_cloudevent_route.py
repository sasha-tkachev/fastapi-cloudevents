from fastapi_cloudevents.cloudevent_route import CloudEventRoute
from fastapi_cloudevents.settings import CloudEventSettings


def test_route_is_configurable():
    dummy_settings = CloudEventSettings()
    assert CloudEventRoute._settings is not dummy_settings
    assert CloudEventRoute.configured(dummy_settings)._settings == dummy_settings

