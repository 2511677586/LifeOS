# Ability List

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

## Ability-0012 — Knowledge Linking
- Ability ID: Ability-0012
- Name: Knowledge Linking
- Purpose: Add explicit relationships between knowledge records.
- Expected user value: Users can connect related ideas and build a knowledge graph.
- Main architectural layer: Service Layer
- Dependencies: Ability-0009 Knowledge Query, Ability-0011 Knowledge Relations
- Status: Planned

## Ability-0013 — Knowledge Browser
- Ability ID: Ability-0013
- Name: Knowledge Browser
- Purpose: Provide a dedicated browsing experience for structured knowledge.
- Expected user value: Users can navigate their knowledge base beyond recent captures.
- Main architectural layer: Presentation Layer
- Dependencies: Ability-0009 Knowledge Query, Ability-0010 Knowledge Types, Ability-0011 Knowledge Relations, Ability-0012 Knowledge Linking
- Status: Planned
