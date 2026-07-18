from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class KnowledgeRelation:
    """Directed relation between two Knowledge Objects.

    source_id and target_id must be stable Knowledge IDs. Referential integrity
    against repositories is intentionally deferred in this milestone to avoid
    incomplete coupling between relation business rules and persistence.
    """

    source_id: str
    relation_type: str
    target_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
