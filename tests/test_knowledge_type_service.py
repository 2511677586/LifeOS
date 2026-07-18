from __future__ import annotations

import unittest
import warnings

from app.services.knowledge_type_service import KnowledgeTypeService


class KnowledgeTypeServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = KnowledgeTypeService()

    def test_valid_types_are_supported(self) -> None:
        for knowledge_type in (
            "journal",
            "idea",
            "meeting",
            "project",
            "document",
            "photo",
            "video",
            "conversation",
            "book",
            "article",
            "person",
            "place",
            "event",
        ):
            self.assertTrue(self.service.is_supported_type(knowledge_type))

    def test_unknown_types_warn_but_do_not_break(self) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            normalized = self.service.validate_type("task")
        self.assertEqual(normalized, "task")
        self.assertTrue(any("Unsupported knowledge type" in str(item.message) for item in caught))

    def test_legacy_aliases_are_canonicalized(self) -> None:
        self.assertEqual(self.service.validate_type("memory"), "journal")
        self.assertEqual(self.service.validate_type("note"), "document")

    def test_normalization_is_lowercase_and_trimmed(self) -> None:
        self.assertEqual(self.service.normalize_type("  IDEA  "), "idea")
        self.assertEqual(self.service.validate_type("  PROJECT  "), "project")

    def test_default_type_is_journal(self) -> None:
        self.assertEqual(self.service.default_type(), "journal")


if __name__ == "__main__":
    unittest.main()
