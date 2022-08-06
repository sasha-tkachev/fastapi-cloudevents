from fastapi_cloudevents.cloudevent_route import (_CloudEventRoute,
                                                  cloudevent_route_class)
from fastapi_cloudevents.settings import CloudEventSettings


def test_route_is_configurable():
    dummy_settings = CloudEventSettings()
    assert _CloudEventRoute._settings is not dummy_settings
    assert cloudevent_route_class(dummy_settings)._settings == dummy_settings


def test_route_class_has_default_settings():
    assert cloudevent_route_class()._settings is not None
