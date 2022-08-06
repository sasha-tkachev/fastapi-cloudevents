from fastapi_cloudevents import CloudEventRoute
from fastapi_cloudevents.settings import CloudEventRouteSettings


def test_route_is_configurable():
    dummy_settings = CloudEventRouteSettings()
    assert CloudEventRoute._settings is not dummy_settings
    assert CloudEventRoute.configured(dummy_settings)._settings == dummy_settings
