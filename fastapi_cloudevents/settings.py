from typing import Optional

from pydantic import BaseSettings
from pydantic.types import constr


class CloudEventSettings(BaseSettings):
    default_source: Optional[constr(min_length=1)]
