from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class KnowledgeMetadata:
    id: str
    created_at: datetime
    updated_at: datetime
    type: str
    title: str
    tags: list[str] = field(default_factory=list)
    source: str = "manual"
    version: int = 1
