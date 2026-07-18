from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.storage_service import StorageService


class KnowledgeRepositoryTests(unittest.TestCase):
    def test_save_and_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            repository = KnowledgeRepository(storage_service=storage_service)
            record_id = "knowledge-20260718-000001-aaaaaa"
            document = "---\ntitle: \"Sample\"\n---\n\nBody"

            saved_path = repository.save(record_id, document)
            loaded_content = repository.load(record_id)

            self.assertTrue(saved_path.exists())
            self.assertEqual(loaded_content, document)

    def test_update_existing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            repository = KnowledgeRepository(storage_service=storage_service)
            record_id = "knowledge-20260718-000002-bbbbbb"
            repository.save(record_id, "old")

            repository.update(record_id, "new")

            self.assertEqual(repository.load(record_id), "new")

    def test_update_missing_record_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            repository = KnowledgeRepository(storage_service=storage_service)
            with self.assertRaises(FileNotFoundError):
                repository.update("knowledge-20260718-000003-cccccc", "content")

    def test_delete_existing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            repository = KnowledgeRepository(storage_service=storage_service)
            record_id = "knowledge-20260718-000004-dddddd"
            path = repository.save(record_id, "content")

            repository.delete(record_id)

            self.assertFalse(path.exists())

    def test_list_keeps_legacy_markdown_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            repository = KnowledgeRepository(storage_service=storage_service)
            legacy_path = Path(temp_dir) / "legacy.md"
            legacy_content = "Legacy content without front matter"
            legacy_path.write_text(legacy_content, encoding="utf-8")

            records = repository.list()

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].content, legacy_content)


if __name__ == "__main__":
    unittest.main()
