# Search Foundation Architecture

## 1. Search Vision

Search in LifeOS is not only file lookup.
It is a staged capability that must evolve incrementally while preserving existing boundaries.

Search evolution stages:

- exact filtering
- plain text search
- indexed search
- ranked search
- semantic retrieval
- AI-assisted retrieval

Each stage must be additive, backward compatible, and replaceable.

## 2. Query versus Search

Knowledge Query focuses on structured filtering:

- type
- tags
- dates
- stable IDs

Search focuses on matching user-entered text against knowledge content and metadata.

Separation rule:

- Search may use Query.
- Query must not depend on Search.

## 3. Search Architecture Layers

Future structure:

Presentation Layer
-> Search Service
-> Search Engine
-> Knowledge Query Service
-> Knowledge Repository
-> Storage Service
-> Markdown

```mermaid
flowchart LR
    A[Presentation Layer] --> B[Search Service]
    B --> C[Search Engine]
    C --> D[Knowledge Query Service]
    D --> E[Knowledge Repository]
    E --> F[Storage Service]
    F --> G[Markdown]
```

## 4. Search Service Responsibility

SearchService is the stable application-facing entry point.

Responsibilities:

- accept a search request
- validate input
- coordinate search engines
- apply filters
- return SearchResult objects

Boundary rule:

- SearchService must not directly read Markdown files.

## 5. Search Engine Boundary

SearchEngine must be a replaceable interface.

Possible implementations:

- PlainTextSearchEngine
- Future SQLiteIndexSearchEngine
- Future SemanticSearchEngine
- Future HybridSearchEngine

No engine implementation is introduced in this ability.

## 6. Search Request Model

Future SearchRequest conceptual fields:

- query_text
- knowledge_types
- tags
- date_from
- date_to
- limit
- sort_order
- include_content
- future semantic options

This section defines architecture only; no source model is created in this sprint.

## 7. Search Result Model

Future SearchResult conceptual fields:

- knowledge_id
- title
- knowledge_type
- matched_text
- match_source
- score
- occurred_at
- path or repository reference
- metadata

UI must consume SearchResult objects instead of raw file paths.

## 8. Exact Filtering

Structured filters remain in KnowledgeQueryService:

- type
- tag
- date range
- stable ID

Search must reuse existing query logic and must not duplicate it.

## 9. Plain Text Search

First implementation stage:

- scan Knowledge Objects through query/repository boundaries
- match query_text against content and selected metadata fields
- preserve compatibility with existing Markdown files

Boundary rule:

- UI must not scan files directly.

## 10. Future SQLite Index

SQLite is planned only as an index or cache.

Rules:

- Markdown remains source of truth.
- The index must be rebuildable from Markdown.
- Losing the index must not lose knowledge.
- SearchService must not depend permanently on SQLite.

## 11. Future Semantic Search

Future capabilities may include:

- embeddings
- semantic similarity
- hybrid search
- AI retrieval

Derived-data rule:

- embeddings and AI-generated metadata are derived data.
- derived data is not source-of-truth data.

## 12. Ranking

Future ranking signals may include:

- exact title match
- metadata match
- content match
- recency
- relation relevance
- semantic score

A final ranking algorithm is intentionally deferred.

## 13. Backward Compatibility

Search must handle:

- old Markdown files without complete front matter
- missing type
- missing occurred_at
- unknown metadata fields
- malformed records that remain recoverable

Compatibility rule:

- parse defensively, return partial results when possible, avoid destructive behavior.

## 14. Service Boundaries

Explicitly prohibited:

- UI reading Markdown directly
- SearchService bypassing KnowledgeRepository
- search engines modifying source files
- SQLite becoming source of truth
- AI rewriting knowledge during search
- product-specific search logic inside the shared core

## 15. Platform Reuse

Possible validation domains:

- LifeOS: journals, conversations, photos, personal records
- MineSystem: shipments, containers, vehicles, laboratory reports
- ICE Studio: stories, scenes, characters, worlds

These are validation examples only.
No cross-project runtime dependencies are introduced.

## 16. Initial Ability Roadmap

Proposed Search Foundation sequence:

- Ability-0013 Search Architecture
- Ability-0014 Plain Text Search
- Ability-0015 Search Result Model
- Ability-0016 Search Ranking
- Ability-0017 Search UI
- Architecture Sprint-003 Search Foundation Closure

## 17. Deferred Capabilities

Deferred in this ability:

- SQLite index
- semantic search
- embeddings
- AI retrieval
- hybrid ranking
- graph-aware search
- OCR
- image search
- cloud search
- cross-device synchronization

## 18. Design Principles

- Markdown First
- Search Through Services
- Query and Search Separation
- Replaceable Search Engines
- Rebuildable Indexes
- Backward Compatibility
- Human Recoverability
- Platform Reusability
- Incremental Evolution
- No AI Dependency

## 19. Completion Statement

Ability-0014 implementation may begin only after this Search Foundation architecture document is reviewed.

## Appendix: Consistency Review Note

Reviewed reference set:

- docs/MasterPlan.md
- docs/Architecture.md
- docs/KnowledgeArchitecture.md
- docs/Milestone2KnowledgeFoundation.md
- docs/Roadmap.md

Note:

- Constitution.md was not found in the current repository at review time.
