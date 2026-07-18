from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class KnowledgeTime:
    """Temporal model for a Knowledge Object.

    Semantics:
    - created_at: when the object was created in LifeOS.
    - updated_at: when the object was last changed in LifeOS.
    - occurred_at: when the represented real-world event happened.

    Optional fields are included for future compatibility and must not force
    product-specific timeline behavior at this stage.
    """

    created_at: datetime
    updated_at: datetime
    occurred_at: datetime | None = None
    ended_at: datetime | None = None
    timezone: str | None = None
    precision: str | None = None
    source: str | None = None
