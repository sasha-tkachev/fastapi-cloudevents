import typing

import cloudevents.pydantic
import pydantic


class CloudEvent(cloudevents.pydantic.CloudEvent):
    """
    Same as the official pydantic CloudEvent model, but if no source is given,
    The source will be injected via the CloudEvent response class.
    """

    source: typing.Optional[str] = pydantic.Field(
        title="Event Source",
        description=(
            "Identifies the context in which an event happened. Often this will include"
            " information such as the type of the event source, the organization"
            " publishing the event or the process that produced the event. The exact"
            " syntax and semantics behind the data encoded in the URI is defined by the"
            " event producer.\n"
            "\n"
            "Producers MUST ensure that source + id is unique for"
            " each distinct event.\n"
            "\n"
            "An application MAY assign a unique source to each"
            " distinct producer, which makes it easy to produce unique IDs since no"
            " other producer will have the same source. The application MAY use UUIDs,"
            " URNs, DNS authorities or an application-specific scheme to create unique"
            " source identifiers.\n"
            "\n"
            "A source MAY include more than one producer. In"
            " that case the producers MUST collaborate to ensure that source + id is"
            " unique for each distinct event."
        ),
    )
