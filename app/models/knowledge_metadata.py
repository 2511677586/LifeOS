from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class KnowledgeMetadata:
    """Standard metadata envelope for a Knowledge Object.

    This model is shared across the service layer and Markdown front matter
    serialization to keep knowledge records both human-readable and
    machine-readable.
    """

    id: str
    title: str
    type: str
    created: datetime
    updated: datetime
    tags: list[str] = field(default_factory=list)
    source: str = "manual"
    version: int = 1
