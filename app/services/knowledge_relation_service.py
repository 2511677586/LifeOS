from __future__ import annotations

import warnings
from typing import Any

from app.models.knowledge_relation import KnowledgeRelation
from app.models.knowledge_relation_types import STANDARD_RELATION_TYPES


class KnowledgeRelationService:
    """Service-layer manager for Knowledge Object relations.

    This service owns relation business rules and in-memory relation operations.
    Persistence integration is intentionally deferred to keep storage concerns
    separated until a stable Markdown relation representation is introduced.

    TODO: Introduce a repository-backed relation persistence adapter once the
    Markdown relation storage format is finalized.
    """

    def __init__(self, relations: list[KnowledgeRelation] | None = None) -> None:
        self._relations: list[KnowledgeRelation] = list(relations or [])

    def create_relation(
        self,
        source_id: str,
        relation_type: str,
        target_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> KnowledgeRelation:
        """Create and store a normalized relation entry."""
        relation = KnowledgeRelation(
            source_id=source_id,
            relation_type=self.normalize_relation_type(relation_type),
            target_id=target_id,
            metadata=dict(metadata or {}),
        )
        self.validate_relation(relation)
        self._relations.append(relation)
        return relation

    def validate_relation(self, relation: KnowledgeRelation) -> None:
        """Validate stable IDs and relation type compatibility.

        Referential integrity is deferred: source and target records are not
        required to exist in repositories during this milestone.
        """
        if not relation.source_id.strip():
            raise ValueError("Relation source_id cannot be empty.")
        if not relation.target_id.strip():
            raise ValueError("Relation target_id cannot be empty.")

        normalized_type = self.normalize_relation_type(relation.relation_type)
        if normalized_type not in STANDARD_RELATION_TYPES:
            supported = ", ".join(STANDARD_RELATION_TYPES)
            warnings.warn(
                (
                    f"Unknown relation type '{relation.relation_type}'. "
                    "Relation remains readable for backward compatibility. "
                    f"Standard relation types: {supported}"
                ),
                UserWarning,
                stacklevel=2,
            )
        relation.relation_type = normalized_type

    def normalize_relation_type(self, relation_type: str) -> str:
        """Normalize relation type values into lowercase, underscore-safe text."""
        normalized = relation_type.strip().lower().replace(" ", "_")
        return normalized

    def list_outgoing_relations(self, source_id: str) -> list[KnowledgeRelation]:
        """List relations where source_id matches."""
        if not source_id.strip():
            raise ValueError("source_id cannot be empty.")
        return [relation for relation in self._relations if relation.source_id == source_id]

    def list_incoming_relations(self, target_id: str) -> list[KnowledgeRelation]:
        """List relations where target_id matches."""
        if not target_id.strip():
            raise ValueError("target_id cannot be empty.")
        return [relation for relation in self._relations if relation.target_id == target_id]

    def remove_relation(self, source_id: str, relation_type: str, target_id: str) -> bool:
        """Remove a matching relation and return whether it was removed."""
        normalized_type = self.normalize_relation_type(relation_type)
        for index, relation in enumerate(self._relations):
            if (
                relation.source_id == source_id
                and relation.relation_type == normalized_type
                and relation.target_id == target_id
            ):
                self._relations.pop(index)
                return True
        return False
