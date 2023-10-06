from enum import Enum
from typing import Optional

from pydantic import StringConstraints, Field

from typing_extensions import Annotated
from pydantic_settings import BaseSettings


class ContentMode(Enum):
    binary = "binary"
    structured = "structured"


class CloudEventSettings(BaseSettings):
    default_source: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    default_response_mode: ContentMode = ContentMode.binary
    allow_non_cloudevent_models: bool = Field(
        default=True,
        description="When allowed, will not fail on non-CloudEvent objects",
    )
