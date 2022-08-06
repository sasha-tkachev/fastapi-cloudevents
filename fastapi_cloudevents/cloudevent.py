import cloudevents.pydantic

DEFAULT_SOURCE = "fastapi"


class CloudEvent(cloudevents.pydantic.CloudEvent):
    """
    Same as the official pydantic CloudEvent model, but if no source is given,
    The source will be injected via the CloudEvent response class.
    """

    source: str = DEFAULT_SOURCE
