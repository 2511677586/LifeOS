from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.models.knowledge_metadata import KnowledgeMetadata
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
    - Delegate to StorageService where safe and available.

    Non-goals in this phase:
    - Search implementation.
    - AI integration.
    - Database-backed primary storage.
    """

    def __init__(
        self,
        storage_service: StorageService | None = None,
        metadata_service: MetadataService | None = None,
    ) -> None:
        self._storage_service = storage_service or StorageService()
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
        standard metadata envelope before being saved via StorageService.

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
        path = self._storage_service.save_markdown(metadata.id, document)
        return SavedKnowledge(metadata=metadata, path=path, document=document)

    def load_knowledge(self, knowledge_id: str) -> str:
        """Load a knowledge document by stable knowledge ID.

        This placeholder resolves the existing Markdown path convention and
        reads content via StorageService.
        """
        record_path = self._resolve_record_path(knowledge_id)
        return self._storage_service.read_markdown(record_path)

    def update_knowledge(self, knowledge_id: str, document: str) -> Path:
        """Update an existing knowledge document.

        TODO: Add richer update semantics and optimistic conflict handling.
        Currently this reuses the existing save behavior to preserve compatibility.
        """
        if not self._storage_service.record_exists(knowledge_id):
            raise FileNotFoundError(f"Knowledge record not found: {knowledge_id}")
        return self._storage_service.save_markdown(knowledge_id, document)

    def delete_knowledge(self, knowledge_id: str) -> None:
        """Delete a knowledge document by stable knowledge ID.

        TODO: Introduce soft-delete, archive policy, and relation-safe deletion.
        """
        record_path = self._resolve_record_path(knowledge_id)
        record_path.unlink()

    def list_knowledge(self, limit: int = 20) -> list[StoredRecord]:
        """List recent knowledge records.

        Placeholder implementation delegates to existing storage listing behavior.
        """
        return self._storage_service.list_recent_records(limit=limit)

    def _resolve_record_path(self, knowledge_id: str) -> Path:
        if not self._storage_service.record_exists(knowledge_id):
            raise FileNotFoundError(f"Knowledge record not found: {knowledge_id}")
        records_dir = getattr(
            self._storage_service,
            "_records_dir",
            Path(__file__).resolve().parents[2] / "data" / "records",
        )
        return records_dir / f"{knowledge_id}.md"
