from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.models.knowledge_metadata import KnowledgeMetadata
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.knowledge_query_service import KnowledgeQueryService
from app.services.metadata_service import MetadataService
from app.services.storage_service import StoredRecord, StorageService


@dataclass(slots=True)
class SavedKnowledge:
    metadata: KnowledgeMetadata
    path: Path
    document: str


class KnowledgeService:
    """Unified entry point for knowledge operations.

    This service forms the Knowledge Layer between the UI-facing services and the
    storage layer. It centralizes knowledge-oriented operations so business logic
    does not leak into the UI layer.

    Current scope:
    - Preserve existing Markdown storage behavior.
    - Provide placeholder CRUD/list methods for future development.
    - Delegate persistence to KnowledgeRepository.

    Non-goals in this phase:
    - Search implementation.
    - AI integration.
    - Database-backed primary storage.
    """

    def __init__(
        self,
        knowledge_repository: KnowledgeRepository | None = None,
        knowledge_query_service: KnowledgeQueryService | None = None,
        storage_service: StorageService | None = None,
        metadata_service: MetadataService | None = None,
    ) -> None:
        resolved_storage_service = storage_service or StorageService()
        self._knowledge_repository = knowledge_repository or KnowledgeRepository(storage_service=resolved_storage_service)
        self._knowledge_query_service = knowledge_query_service or KnowledgeQueryService(self._knowledge_repository)
        self._metadata_service = metadata_service or MetadataService()

    def create_knowledge(
        self,
        content: str,
        *,
        title: str | None = None,
        knowledge_type: str | None = None,
        tags: list[str] | None = None,
        source: str = "manual",
    ) -> SavedKnowledge:
        """Create and persist a knowledge document as Markdown.

        This integrates the Metadata layer so new Knowledge Objects receive a
        standard metadata envelope before being saved via KnowledgeRepository.

        TODO: Route all UI knowledge-write entry points through this method.
        """
        cleaned_content = content.strip()
        if not cleaned_content:
            raise ValueError("Content cannot be empty.")

        metadata = self._metadata_service.create_metadata(
            cleaned_content,
            title=title,
            knowledge_type=knowledge_type,
            tags=tags,
            source=source,
        )
        document = self._metadata_service.build_markdown_document(cleaned_content, metadata)
        path = self._knowledge_repository.save(metadata.id, document)
        return SavedKnowledge(metadata=metadata, path=path, document=document)

    def load_knowledge(self, knowledge_id: str) -> str:
        """Load a knowledge document by stable knowledge ID.

        This delegates retrieval concerns to KnowledgeQueryService.
        """
        record = self._knowledge_query_service.get_by_id(knowledge_id)
        if record is None:
            raise FileNotFoundError(f"Knowledge record not found: {knowledge_id}")
        return record.content

    def update_knowledge(self, knowledge_id: str, document: str) -> Path:
        """Update an existing knowledge document.

        TODO: Add richer update semantics and optimistic conflict handling.
        Persistence is delegated to KnowledgeRepository.
        """
        return self._knowledge_repository.update(knowledge_id, document)

    def delete_knowledge(self, knowledge_id: str) -> None:
        """Delete a knowledge document by stable knowledge ID.

        TODO: Introduce soft-delete, archive policy, and relation-safe deletion.
        """
        self._knowledge_repository.delete(knowledge_id)

    def list_knowledge(self, limit: int = 20) -> list[StoredRecord]:
        """List recent knowledge records.

        Placeholder implementation delegates to query layer listing behavior.
        """
        return self._knowledge_query_service.list_all()[:limit]

    def filter_knowledge_by_type(self, knowledge_type: str) -> list[StoredRecord]:
        """Filter knowledge records by type through the query layer."""
        return self._knowledge_query_service.filter_by_type(knowledge_type)

    def filter_knowledge_by_tag(self, tag: str) -> list[StoredRecord]:
        """Filter knowledge records by tag through the query layer."""
        return self._knowledge_query_service.filter_by_tag(tag)

    def filter_knowledge_by_date_range(self, start_date: datetime, end_date: datetime) -> list[StoredRecord]:
        """Filter knowledge records by created date range through the query layer."""
        return self._knowledge_query_service.filter_by_date_range(start_date, end_date)
