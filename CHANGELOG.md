# Changelog

## Unreleased
- Initial project documentation for the LifeOS knowledge foundation.

### Added
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
