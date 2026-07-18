# Ability List

## Architecture Sprint-002 — Milestone 2 Knowledge Foundation Closure
- Sprint ID: Architecture Sprint-002
- Name: Milestone 2 Knowledge Foundation Closure
- Purpose: Formally close Milestone 2 with architecture validation, consistency review, and milestone completion documentation.
- Main architectural layer: Architecture Governance
- Dependencies: Ability-0006 through Ability-0012 completed
- Status: Completed

## Ability-0006 — Knowledge Service
- Ability ID: Ability-0006
- Name: Knowledge Service
- Purpose: Establish a unified service-layer entry point for knowledge operations while preserving existing Markdown behavior.
- Expected user value: Provides a stable architecture boundary for future knowledge CRUD, indexing, and automation without changing current user workflow.
- Main architectural layer: Service Layer
- Dependencies: Milestone 1 capture flow, Markdown storage, stable record save workflow
- Status: Completed

## Ability-0007 — Knowledge Metadata
- Ability ID: Ability-0007
- Name: Knowledge Metadata
- Purpose: Establish the standard metadata model and service lifecycle for Knowledge Objects.
- Expected user value: Knowledge records remain human-readable while gaining consistent machine-readable metadata for future capabilities.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Service
- Status: Completed

## Ability-0008 — Knowledge Repository
- Ability ID: Ability-0008
- Name: Knowledge Repository
- Purpose: Introduce a dedicated repository layer responsible only for Knowledge Object persistence.
- Expected user value: Improves architecture stability by separating service orchestration from persistence concerns.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Service, Ability-0007 Knowledge Metadata
- Status: Completed

## Ability-0009 — Knowledge Query
- Ability ID: Ability-0009
- Name: Knowledge Query
- Purpose: Introduce a dedicated query layer for retrieval and metadata-based filtering of Knowledge Objects.
- Expected user value: Enables structured read operations without coupling UI or orchestration logic to persistence details.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Service, Ability-0008 Knowledge Repository
- Status: Completed

## Ability-0010 — Knowledge Types
- Ability ID: Ability-0010
- Name: Knowledge Types
- Purpose: Standardize and validate metadata type values across service and query layers.
- Expected user value: Keeps knowledge classification consistent while preserving readability of legacy and custom type data.
- Main architectural layer: Service Layer
- Dependencies: Ability-0009 Knowledge Query
- Status: Completed

## Ability-0011 — Knowledge Relations
- Ability ID: Ability-0011
- Name: Knowledge Relations
- Purpose: Establish a reusable relation model and service layer for connecting Knowledge Objects.
- Expected user value: Enables future graph, timeline, and cross-domain context without coupling relation logic to UI or storage.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Service, Ability-0009 Knowledge Query, Ability-0010 Knowledge Types
- Status: Completed

## Ability-0012 — Timeline Foundation
- Ability ID: Ability-0012
- Name: Timeline Foundation
- Purpose: Establish a platform-oriented time model and timeline service for temporal retrieval and grouping.
- Expected user value: Enables future timeline/map experiences while preserving backward-compatible Markdown workflows.
- Main architectural layer: Service Layer
- Dependencies: Ability-0007 Knowledge Metadata, Ability-0009 Knowledge Query, Ability-0010 Knowledge Types
- Status: Completed

## Ability-0013 — Search Architecture
- Ability ID: Ability-0013
- Name: Search Architecture
- Purpose: Define the Search Foundation architecture while preserving existing Knowledge Foundation boundaries.
- Expected user value: Enables safe incremental search evolution without breaking source-of-truth and service boundaries.
- Main architectural layer: Architecture Governance
- Dependencies: Ability-0006 through Ability-0012 completed
- Status: Completed

## Ability-0014 — Plain Text Search
- Ability ID: Ability-0014
- Name: Plain Text Search
- Purpose: Implement boundary-safe plain text matching through service/query/repository layers.
- Expected user value: Users can search text in knowledge content and metadata.
- Main architectural layer: Service Layer
- Dependencies: Ability-0013 Search Architecture
- Status: Planned

## Ability-0015 — Search Result Model
- Ability ID: Ability-0015
- Name: Search Result Model
- Purpose: Introduce a stable SearchResult contract for UI and future consumers.
- Expected user value: Consistent, explainable search outputs independent of storage paths.
- Main architectural layer: Service Layer
- Dependencies: Ability-0013 Search Architecture, Ability-0014 Plain Text Search
- Status: Planned

## Ability-0016 — Search Ranking
- Ability ID: Ability-0016
- Name: Search Ranking
- Purpose: Add ranking logic across exact, metadata, and recency signals.
- Expected user value: More relevant search result ordering.
- Main architectural layer: Service Layer
- Dependencies: Ability-0014 Plain Text Search, Ability-0015 Search Result Model
- Status: Planned

## Ability-0017 — Search UI
- Ability ID: Ability-0017
- Name: Search UI
- Purpose: Provide a dedicated search interaction in the presentation layer using SearchResult outputs.
- Expected user value: Usable, structured search experience.
- Main architectural layer: Presentation Layer
- Dependencies: Ability-0014 Plain Text Search, Ability-0015 Search Result Model, Ability-0016 Search Ranking
- Status: Planned

## Architecture Sprint-003 — Search Foundation Closure
- Sprint ID: Architecture Sprint-003
- Name: Search Foundation Closure
- Purpose: Validate and formally close Search Foundation architecture and boundaries.
- Main architectural layer: Architecture Governance
- Dependencies: Ability-0013 through Ability-0017
- Status: Planned
