from __future__ import annotations

from pathlib import Path

from app.services.storage_service import StoredRecord, StorageService


class KnowledgeRepository:
    """Repository layer for Knowledge Object persistence.

    Responsibility is limited to persistence operations and compatibility with
    the existing Markdown storage model. This repository delegates all file
    mechanics to StorageService and exposes a stable CRUD/list interface for
    the service layer.
    """

    def __init__(self, storage_service: StorageService | None = None) -> None:
        self._storage_service = storage_service or StorageService()

    def save(self, knowledge_id: str, document: str) -> Path:
        """Persist a new knowledge document."""
        return self._storage_service.save_markdown(knowledge_id, document)

    def load(self, knowledge_id: str) -> str:
        """Load a knowledge document by stable knowledge ID."""
        record_path = self._resolve_record_path(knowledge_id)
        return self._storage_service.read_markdown(record_path)

    def update(self, knowledge_id: str, document: str) -> Path:
        """Update an existing knowledge document."""
        if not self._storage_service.record_exists(knowledge_id):
            raise FileNotFoundError(f"Knowledge record not found: {knowledge_id}")
        return self._storage_service.save_markdown(knowledge_id, document)

    def delete(self, knowledge_id: str) -> None:
        """Delete a knowledge document by stable knowledge ID."""
        record_path = self._resolve_record_path(knowledge_id)
        record_path.unlink()

    def list(self, limit: int = 20) -> list[StoredRecord]:
        """List recent knowledge records from Markdown storage."""
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
