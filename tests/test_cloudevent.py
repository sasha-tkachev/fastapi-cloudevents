from fastapi_cloudevents import CloudEvent
from fastapi_cloudevents.cloudevent import DEFAULT_SOURCE


def test_fastapi_cloudevent_has_a_default_source():
    assert CloudEvent(type="my.type.v1").source == DEFAULT_SOURCE
