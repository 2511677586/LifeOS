from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.knowledge_query_service import KnowledgeQueryService
from app.services.storage_service import StorageService


class KnowledgeQueryServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        storage_service = StorageService(records_dir=Path(self._temp_dir.name))
        repository = KnowledgeRepository(storage_service=storage_service)
        self.service = KnowledgeQueryService(repository)

        self._write_record(
            "knowledge-001",
            (
                "---\n"
                "id: \"knowledge-001\"\n"
                "type: \"journal\"\n"
                "tags: [\"life\", \"personal\"]\n"
                "created: \"2026-07-10T08:00:00+00:00\"\n"
                "---\n\n"
                "Journal content"
            ),
        )
        self._write_record(
            "knowledge-002",
            (
                "---\n"
                "id: \"knowledge-002\"\n"
                "type: \"project\"\n"
                "tags: [\"work\", \"planning\"]\n"
                "created: \"2026-07-15T08:00:00+00:00\"\n"
                "---\n\n"
                "Project content"
            ),
        )
        self._write_record(
            "knowledge-legacy",
            (
                "---\n"
                "id: \"knowledge-legacy\"\n"
                "type: \"memory\"\n"
                "tags: [\"archive\"]\n"
                "created_at: \"2026-07-12T10:30:00+00:00\"\n"
                "---\n\n"
                "Legacy metadata key content"
            ),
        )
        self._write_record("legacy-no-front-matter", "Legacy content without front matter")

    def tearDown(self) -> None:
        self._temp_dir.cleanup()

    def test_list_all_returns_all_records(self) -> None:
        records = self.service.list_all()
        self.assertEqual(len(records), 4)

    def test_get_by_id_returns_matching_record(self) -> None:
        record = self.service.get_by_id("knowledge-002")
        self.assertIsNotNone(record)
        assert record is not None
        self.assertIn("Project content", record.content)

    def test_get_by_id_returns_none_when_missing(self) -> None:
        record = self.service.get_by_id("missing")
        self.assertIsNone(record)

    def test_filter_by_type(self) -> None:
        records = self.service.filter_by_type("journal")
        record_ids = {record.path.stem for record in records}
        self.assertEqual(record_ids, {"knowledge-001", "knowledge-legacy"})

    def test_filter_by_type_uses_standardized_aliases(self) -> None:
        records = self.service.filter_by_type("memory")
        record_ids = {record.path.stem for record in records}
        self.assertEqual(record_ids, {"knowledge-001", "knowledge-legacy"})

    def test_filter_by_tag_is_case_insensitive(self) -> None:
        records = self.service.filter_by_tag("WORK")
        record_ids = {record.path.stem for record in records}
        self.assertEqual(record_ids, {"knowledge-002"})

    def test_filter_by_date_range_supports_created_and_created_at(self) -> None:
        start = datetime(2026, 7, 11, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 7, 13, 0, 0, tzinfo=timezone.utc)
        records = self.service.filter_by_date_range(start, end)
        record_ids = {record.path.stem for record in records}
        self.assertEqual(record_ids, {"knowledge-legacy"})

    def _write_record(self, record_id: str, content: str) -> None:
        path = Path(self._temp_dir.name) / f"{record_id}.md"
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
