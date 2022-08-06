from enum import Enum
from typing import Optional

from pydantic import BaseSettings, Field
from pydantic.types import constr


class ResponseMode(Enum):
    binary = "binary"
    structured = "structured"


class CloudEventSettings(BaseSettings):
    default_source: Optional[constr(min_length=1)]
    default_response_mode: ResponseMode = ResponseMode.binary
    allow_non_cloudevent_models: bool = Field(
        default=True,
        description="When allowed, will not fail on non-CloudEvent objects",
    )
