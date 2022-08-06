from enum import Enum
from typing import Optional

from pydantic import BaseSettings
from pydantic.types import constr


class ResponseMode(Enum):
    binary = "binary"
    structured = "structured"


class CloudEventSettings(BaseSettings):
    default_source: Optional[constr(min_length=1)]
    default_response_mode: ResponseMode = ResponseMode.binary
