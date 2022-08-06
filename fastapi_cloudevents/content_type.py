import re
import typing

# https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md#311-payload-serialization
_JSON_CONTENT_TYPE_PATTERN = re.compile(
    r"^(.*/.*json|.*/.*\+json)$", flags=re.IGNORECASE
)


def is_json_content_type(data_content_type: typing.Optional[str]) -> bool:
    """
    Assuming asking about the datacontenttype attribute value
    """
    if data_content_type is None:
        # according to spec:  an event with no datacontenttype is exactly equivalent to
        # one with datacontenttype="application/json".
        return True
    return bool(_JSON_CONTENT_TYPE_PATTERN.match(data_content_type))
