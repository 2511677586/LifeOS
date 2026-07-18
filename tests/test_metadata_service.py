from __future__ import annotations

import unittest
from datetime import datetime, timezone

from app.models.knowledge_metadata import KnowledgeMetadata
from app.services.knowledge_type_service import KnowledgeTypeService
from app.services.metadata_service import MetadataService


class MetadataServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = MetadataService()

    def test_first_meaningful_line_becomes_title(self) -> None:
        title = self.service.generate_title("\n\n# Today’s project idea\nMore text")
        self.assertEqual(title, "Today’s project idea")

    def test_empty_lines_do_not_become_title(self) -> None:
        title = self.service.generate_title("\n\n   \n# Heading")
        self.assertEqual(title, "Heading")

    def test_long_titles_are_shortened_safely(self) -> None:
        title = self.service.generate_title("This is a very long title that should be shortened safely without breaking the format")
        self.assertLessEqual(len(title), 60)
        self.assertTrue(title.endswith("..."))

    def test_quotes_do_not_break_front_matter(self) -> None:
        metadata = self.service.create_metadata('He said "hello" and \n kept going')
        front_matter = self.service.serialize_front_matter(metadata)
        self.assertIn('title: ', front_matter)
        self.assertIn('\\"hello\\"', front_matter)

    def test_ids_are_different_for_new_records(self) -> None:
        first = self.service.create_metadata("First")
        second = self.service.create_metadata("Second")
        self.assertNotEqual(first.id, second.id)

    def test_timestamps_are_timezone_aware_iso_strings(self) -> None:
        metadata = self.service.create_metadata("Content")
        created = metadata.created
        updated = metadata.updated
        self.assertIsNotNone(created.tzinfo)
        self.assertIsNotNone(updated.tzinfo)
        created_text = self.service._format_datetime(created)
        updated_text = self.service._format_datetime(updated)
        self.assertRegex(created_text, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")
        self.assertRegex(updated_text, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")
        self.assertEqual(created_text, updated_text)

    def test_document_contains_required_front_matter_fields(self) -> None:
        metadata = self.service.create_metadata("Sample content")
        document = self.service.build_markdown_document("Sample content", metadata)
        self.assertTrue(document.startswith("---\n"))
        self.assertIn("id: ", document)
        self.assertIn("created: ", document)
        self.assertIn("updated: ", document)
        self.assertIn("created_at: ", document)
        self.assertIn("updated_at: ", document)
        self.assertIn("type: ", document)
        self.assertIn("title: ", document)
        self.assertIn("tags: []", document)
        self.assertIn("source: ", document)
        self.assertIn("version: 1", document)
        self.assertIn("\n---\n\nSample content", document)

    def test_default_type_is_provided_by_knowledge_type_service(self) -> None:
        class CustomKnowledgeTypeService(KnowledgeTypeService):
            def default_type(self) -> str:
                return "note"

        metadata_service = MetadataService(knowledge_type_service=CustomKnowledgeTypeService())
        metadata = metadata_service.create_metadata("Sample content")
        self.assertEqual(metadata.type, "note")

    def test_update_metadata_refreshes_updated_and_version(self) -> None:
        metadata = self.service.create_metadata("Original")
        updated_metadata = self.service.update_metadata(metadata, title="Updated title", tags=["work", ""])
        self.assertEqual(updated_metadata.title, "Updated title")
        self.assertEqual(updated_metadata.tags, ["work"])
        self.assertGreaterEqual(updated_metadata.updated, metadata.updated)
        self.assertEqual(updated_metadata.version, metadata.version + 1)

    def test_validate_metadata_rejects_invalid_timestamps(self) -> None:
        invalid_metadata = KnowledgeMetadata(
            id="knowledge-20260718-000000-abc123",
            title="Invalid",
            type="memory",
            created=datetime(2026, 7, 18, 8, 0, tzinfo=timezone.utc),
            updated=datetime(2026, 7, 18, 7, 59, tzinfo=timezone.utc),
            tags=[],
            source="manual",
            version=1,
        )
        with self.assertRaises(ValueError):
            self.service.validate_metadata(invalid_metadata)



if __name__ == "__main__":
    unittest.main()
