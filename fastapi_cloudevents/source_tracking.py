from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceTracker:
    source_assigned_to_user: Optional[str] = None
