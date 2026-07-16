from __future__ import annotations

import unittest

from app.services.knowledge_type_service import KnowledgeTypeService


class KnowledgeTypeServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = KnowledgeTypeService()

    def test_valid_types_are_supported(self) -> None:
        for knowledge_type in (
            "memory",
            "idea",
            "project",
            "person",
            "event",
            "decision",
            "reference",
            "note",
        ):
            self.assertTrue(self.service.is_supported_type(knowledge_type))

    def test_invalid_types_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.service.validate_type("task")

    def test_normalization_is_lowercase_and_trimmed(self) -> None:
        self.assertEqual(self.service.normalize_type("  IDEA  "), "idea")
        self.assertEqual(self.service.validate_type("  PROJECT  "), "project")

    def test_default_type_is_memory(self) -> None:
        self.assertEqual(self.service.default_type(), "memory")


if __name__ == "__main__":
    unittest.main()
