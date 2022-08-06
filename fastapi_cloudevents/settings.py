from enum import Enum
from typing import Optional

from pydantic import BaseSettings
from pydantic.types import constr


class ResponseMode(Enum):
    binary = "binary"
    structured = "structured"


class CloudEventSettings(BaseSettings):
    default_source: Optional[constr(min_length=1)]
    response_mode: ResponseMode = ResponseMode.binary
    create_events_on_behalf_of_the_client: bool = False
    default_user_event_type: str = "fastapi.client.request.v1"
    store_assigned_sources_in_cookies: bool = False
    assigned_source_cookie_key: str = "assigned-ce-source"
