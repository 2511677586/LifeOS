from __future__ import annotations

import unittest
import warnings

from app.services.knowledge_relation_service import KnowledgeRelationService


class KnowledgeRelationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = KnowledgeRelationService()

    def test_valid_relation_creation(self) -> None:
        relation = self.service.create_relation(
            source_id="knowledge-001",
            relation_type="related_to",
            target_id="knowledge-002",
            metadata={"confidence": "high"},
        )
        self.assertEqual(relation.source_id, "knowledge-001")
        self.assertEqual(relation.relation_type, "related_to")
        self.assertEqual(relation.target_id, "knowledge-002")
        self.assertEqual(relation.metadata["confidence"], "high")

    def test_empty_source_id_rejection(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_relation("   ", "related_to", "knowledge-002")

    def test_empty_target_id_rejection(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_relation("knowledge-001", "related_to", "   ")

    def test_standard_relation_type_normalization(self) -> None:
        relation = self.service.create_relation("knowledge-001", "  Related To  ", "knowledge-002")
        self.assertEqual(relation.relation_type, "related_to")

    def test_unknown_relation_type_backward_compatibility(self) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            relation = self.service.create_relation("knowledge-001", "custom_link", "knowledge-002")
        self.assertEqual(relation.relation_type, "custom_link")
        self.assertTrue(any("Unknown relation type" in str(item.message) for item in caught))

    def test_outgoing_relation_filtering(self) -> None:
        self.service.create_relation("knowledge-001", "mentions", "knowledge-002")
        self.service.create_relation("knowledge-001", "related_to", "knowledge-003")
        self.service.create_relation("knowledge-004", "related_to", "knowledge-001")

        outgoing = self.service.list_outgoing_relations("knowledge-001")
        self.assertEqual(len(outgoing), 2)
        self.assertEqual({relation.target_id for relation in outgoing}, {"knowledge-002", "knowledge-003"})

    def test_incoming_relation_filtering(self) -> None:
        self.service.create_relation("knowledge-001", "mentions", "knowledge-003")
        self.service.create_relation("knowledge-002", "related_to", "knowledge-003")
        self.service.create_relation("knowledge-003", "follows", "knowledge-004")

        incoming = self.service.list_incoming_relations("knowledge-003")
        self.assertEqual(len(incoming), 2)
        self.assertEqual({relation.source_id for relation in incoming}, {"knowledge-001", "knowledge-002"})

    def test_relation_removal(self) -> None:
        self.service.create_relation("knowledge-001", "mentions", "knowledge-002")
        removed = self.service.remove_relation("knowledge-001", "mentions", "knowledge-002")
        self.assertTrue(removed)
        self.assertEqual(self.service.list_outgoing_relations("knowledge-001"), [])


if __name__ == "__main__":
    unittest.main()
