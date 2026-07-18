from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.services.capture_service import CaptureService
from app.services.metadata_service import MetadataService
from app.services.storage_service import StorageService


class CaptureServiceTests(unittest.TestCase):
    def test_saved_record_contains_front_matter_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            service = CaptureService(metadata_service=MetadataService(), storage_service=storage_service)
            body = "Today’s project idea\nToday’s project idea is to build a searchable personal knowledge system."
            saved_record = service.save_content(body)

            document = saved_record.path.read_text(encoding="utf-8")
            self.assertTrue(document.startswith("---\n"))
            self.assertIn("id: ", document)
            self.assertIn("created: ", document)
            self.assertIn("updated: ", document)
            self.assertIn("created_at: ", document)
            self.assertIn("updated_at: ", document)
            self.assertIn("type: \"journal\"", document)
            self.assertIn("title: \"Today’s project idea\"", document)
            self.assertIn("tags: []", document)
            self.assertIn("source: \"manual\"", document)
            self.assertIn("version: 1", document)
            self.assertTrue(document.endswith(body))

    def test_long_title_is_shortened_in_saved_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            service = CaptureService(metadata_service=MetadataService(), storage_service=storage_service)
            saved_record = service.save_content("This is a very long title that should be shortened safely without breaking the format")

            document = saved_record.path.read_text(encoding="utf-8")
            self.assertIn('title: "This is a very long title that should be shortened safely..."', document)

    def test_two_records_receive_different_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            service = CaptureService(metadata_service=MetadataService(), storage_service=storage_service)
            first = service.save_content("First record")
            second = service.save_content("Second record")
            self.assertNotEqual(first.metadata.id, second.metadata.id)
            self.assertNotEqual(first.path, second.path)

    def test_empty_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            service = CaptureService(metadata_service=MetadataService(), storage_service=storage_service)
            with self.assertRaises(ValueError):
                service.save_content("   \n   ")

    def test_existing_markdown_without_front_matter_can_still_be_browsed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_service = StorageService(records_dir=Path(temp_dir))
            old_record = Path(temp_dir) / "legacy.md"
            old_record.write_text("Legacy content without front matter", encoding="utf-8")

            records = storage_service.list_recent_records()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].content, "Legacy content without front matter")


if __name__ == "__main__":
    unittest.main()
