from __future__ import annotations

import unittest
from datetime import datetime

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
        created = metadata.created_at
        updated = metadata.updated_at
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
        self.assertIn("created_at: ", document)
        self.assertIn("updated_at: ", document)
        self.assertIn("type: ", document)
        self.assertIn("title: ", document)
        self.assertIn("tags: []", document)
        self.assertIn("source: ", document)
        self.assertIn("version: 1", document)
        self.assertIn("\n---\n\nSample content", document)


if __name__ == "__main__":
    unittest.main()
