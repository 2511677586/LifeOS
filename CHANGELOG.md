# Changelog

## Unreleased
- Initial project documentation for the LifeOS knowledge foundation.

### Added
- Added `KnowledgeTime` model and `TimelineService` for timeline normalization, sorting, filtering, and temporal grouping.
- Added timeline fallback precedence (`occurred_at -> created -> created_at -> file timestamp`) for backward compatibility.
- Added unit tests for datetime normalization, occurred_at precedence, range filtering, sorting order, grouping, and missing occurred_at compatibility.
- Extended metadata support with optional `occurred_at` serialization while preserving existing `created`/`updated` compatibility.
- Added `KnowledgeRelation` model and relation type catalog (`knowledge_relation.py`, `knowledge_relation_types.py`).
- Added `KnowledgeRelationService` with create, validate, normalize, list outgoing/incoming, and remove operations.
- Added warning-based backward compatibility for unknown relation types and deferred referential integrity checks.
- Added unit tests for relation creation, ID validation, type normalization, unknown type compatibility, filtering, and removal.
- Added `models/knowledge_types.py` as the centralized Knowledge Type catalog with standard and extension example types.
- Updated `KnowledgeTypeService` to canonicalize legacy aliases and warn on unknown types without breaking existing records.
- Updated `MetadataService` and `KnowledgeQueryService` to use standardized type definitions.
- Added unit tests for Knowledge Type validation, alias canonicalization, warning compatibility, and query type filtering behavior.
- Added `KnowledgeQueryService` with `list_all`, `get_by_id`, `filter_by_type`, `filter_by_tag`, and `filter_by_date_range` methods.
- Added query-layer unit tests for id lookup and metadata-based filtering with legacy compatibility.
- Updated `KnowledgeService` to delegate query-related retrieval operations to `KnowledgeQueryService`.
- Added `KnowledgeRepository` with `save`, `load`, `update`, `delete`, and `list` methods as the dedicated persistence layer for Knowledge Objects.
- Added unit tests for repository save/load/update/delete/list behavior and legacy Markdown compatibility.
- Refactored `KnowledgeService` to delegate persistence operations to `KnowledgeRepository`.
- Added `KnowledgeMetadata` standard model fields (`id`, `title`, `type`, `created`, `updated`, `tags`, `source`, `version`).
- Added `MetadataService.update_metadata()` and `MetadataService.validate_metadata()` for metadata lifecycle management.
- Integrated `KnowledgeService.create_knowledge()` with `MetadataService` for metadata-first knowledge creation.
- Added `KnowledgeService` as the Knowledge Layer entry point with placeholder create/load/update/delete/list methods delegating to the existing storage layer.
- Added official development workflow reference in `docs/DevelopmentWorkflow.md`.
- Added `KnowledgeTypeService` with supported type definitions, normalization, validation, and default type helper methods.
- Updated `MetadataService` to request the default knowledge type from `KnowledgeTypeService`.
- Added unit tests for knowledge type valid values, invalid values, normalization, and default type behavior.
- Structured YAML-style front matter for newly saved Markdown records.
- Stable knowledge IDs for saved records.
- Timezone-aware timestamps in record metadata.
- Generated record titles based on the first meaningful line of content.
- A metadata service that builds and serializes knowledge metadata.
- Backward compatibility for existing Markdown files without front matter.
