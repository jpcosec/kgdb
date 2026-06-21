# KGDB Requirements: Provenance-Aware Knowledge Grounding for Atoms

## Document Status

- Status: Draft
- Audience: KGDB team, deskops maintainers, project knowledge-engineering stakeholders
- Repository: `paper_IEEE`
- Date: 2026-06-19

---

## 1. Executive Summary

This document specifies the KGDB capabilities required to support a provenance-aware knowledge substrate for the ETM/ASI tutoring project.

The project uses **atoms** as stable knowledge units. These atoms are intended to capture theory, data structure, process design, and implementation assumptions related to a two-step mathematics evaluation pipeline:

1. a text-based agent evaluates the ETM demonstrated in student responses
2. an ASI/CHIC postprocessing layer detects cognitive and epistemological incoherences

At present, KGDB can inventory desk artifacts as graph nodes, but it cannot represent the **knowledge origin** of those atoms. It does not yet model:

- source documents as first-class graph nodes
- typed provenance links from atoms to sources
- distinctions between source-grounded, synthesized, and design-derived claims
- reflection checks for unsupported atoms or underused sources

This document defines the requirements needed to make KGDB support those functions.

---

## 2. Context

### 2.1 Project Context

This repository is building the knowledge substrate for an educational system grounded in:

- **ETM** (*Espacio de Trabajo Matemático / Mathematical Working Space*)
- **ASI** (*Análisis Estadístico Implicativo / Implicative Statistical Analysis*)
- **CHIC** tooling for implicative graph construction
- curricular materials, tests, and analysis documents from `source_docs/`

The system requires stable, reviewable knowledge artifacts that can be used by humans and agents.

### 2.2 Why Provenance Matters Here

This project mixes multiple epistemic layers:

- academic theory
- project synthesis documents
- curriculum and evaluation datasets
- implementation decisions made within this repository

These layers must remain distinguishable. Without explicit provenance, atoms become difficult to trust, review, maintain, or query.

### 2.3 Current KGDB State

Current KGDB behavior in this repository demonstrates that it can:

- ingest desk artifacts as nodes
- emit graph snapshots
- record artifact file paths
- report missing graph references known to its current model

However, it does **not** currently:

- ingest `source_docs/` artifacts as first-class source nodes
- create atom-to-source support edges
- understand provenance declarations embedded in desk artifacts
- reflect on orphan atoms lacking grounding

---

## 3. Problem Statement

The current graph model is structurally useful but epistemically insufficient.

KGDB currently knows that:
- an atom exists
- an atom is stored in a desk file

KGDB does **not** know that:
- an atom is supported by a specific source document
- an atom is synthesized from multiple sources
- an atom is a design-derived interpretation rather than a direct source-grounded fact
- a source document has or has not contributed to the knowledge substrate

This prevents the graph from serving as a trustworthy substrate for:

- knowledge review
- auditability
- agentic grounding
- source coverage reflection
- future knowledge maintenance

---

## 4. Goals

KGDB must support a provenance-aware graph model that enables the repository to:

1. represent stable source documents as first-class graph nodes
2. represent typed provenance relations from atoms to sources
3. distinguish different grounding modes
4. expose provenance as machine-readable graph structure
5. support reflection and validation over knowledge grounding
6. support downstream querying for source coverage and trust analysis

---

## 5. Non-Goals

The following are explicitly out of scope for this requirement set unless later requested:

1. OCR or vision-based ingestion of source documents
2. automatic extraction of fine-grained citations from PDFs
3. automatic determination of whether an atom is conceptually correct
4. automatic provenance inference from free prose without explicit declarations
5. scholarly citation formatting or bibliography management
6. trust scoring based on source authority beyond declared provenance
7. full semantic parsing of arbitrary non-desk files outside the declared source catalog

---

## 6. Definitions

### 6.1 Atom
A stable desk artifact representing one focused knowledge unit, structured around one 5W1H+ question shape.

### 6.2 Source Document
A stable document, dataset root, manual, notes file, or source collection that supports one or more atoms.

### 6.3 Provenance
The explicit declaration of where an atom's claim comes from, how it is derived, and how it should be interpreted.

### 6.4 Source-Grounded Claim
A claim directly supported by one or more source documents.

### 6.5 Synthesized Claim
A claim combining multiple source-grounded elements into a higher-level statement not directly stated verbatim in a single source.

### 6.6 Design-Derived Claim
A claim representing a local architectural or implementation decision motivated by the sources but not directly stated in them.

### 6.7 Orphan Atom
An atom with no valid provenance relationship to any declared source node.

---

## 7. Functional Requirements

### FR-1: Canonical Source Catalog Ingestion
KGDB shall ingest a canonical source catalog from a stable project file.

#### Required behavior
- Parse a source catalog file from a stable desk location.
- Create one graph node per declared source entry.
- Validate source identifiers for uniqueness.
- Retain source metadata in the graph snapshot.

#### Minimum source fields
- `id`
- `title`
- `kind`
- `family`
- `path`
- `stability`
- `description`

#### Initial repository target
- `desk/registry/source-catalog.yaml`

---

### FR-2: First-Class Source Nodes
KGDB shall represent source entries as first-class graph nodes.

#### Required node properties
- stable node identity
- node type indicating source semantics
- source metadata from the catalog
- source path preserved in output

#### Suggested node type
- `source_doc`

Alternative naming is acceptable if semantically equivalent and stable.

---

### FR-3: Atom Provenance Declaration Parsing
KGDB shall parse provenance declarations from atom frontmatter or another stable, explicitly defined structured location.

#### Required behavior
- Read provenance declarations from atoms.
- Resolve each declared `source_id` against the canonical source catalog.
- Preserve provenance metadata in the graph.

#### Minimum provenance fields per entry
- `source_id`
- `relation`
- `derivation`

#### Recommended optional fields
- `locator`
- `confidence`
- `notes`

#### Example shape
```yaml
provenance:
  - source_id: source-doc-manual-asi-estructurado
    relation: supported_by
    derivation: paraphrase
    locator: "Parte 1, secciones 1-3"
    confidence: high
```

---

### FR-4: Typed Provenance Edge Emission
KGDB shall create typed edges from atoms to source nodes based on provenance declarations.

#### Required behavior
- Emit a graph edge for each valid provenance entry.
- Preserve relation type and provenance metadata.
- Ensure graph output distinguishes provenance edges from ordinary desk references.

#### Required relation support
At minimum, KGDB shall support:
- `supported_by`
- `synthesized_from`
- `design_derived_from`
- `about_dataset`

#### Optional but desirable later
- `validated_against`
- `contrasted_with`
- `depends_on_source_family`

---

### FR-5: Unknown Source Detection
KGDB shall detect provenance entries that reference unknown `source_id` values.

#### Required behavior
- Do not silently discard unresolved source references.
- Surface them in machine-readable reflection output.
- Associate the error with the offending atom and source identifier.

---

### FR-6: Orphan Atom Detection
KGDB shall detect atoms lacking valid provenance support.

#### Required behavior
- Identify atoms with no provenance declaration.
- Identify atoms whose provenance declarations fail to resolve.
- Report such atoms as orphan or unsupported.

#### Notes
This requirement is essential for knowledge-substrate governance.

---

### FR-7: Source Coverage Reflection
KGDB shall support reflection over source utilization.

#### Required behavior
- Identify source nodes with no incoming support usage from atoms.
- Identify over-centralized source patterns if many atoms depend on a single source.
- Enable coverage review by source family.

#### Examples of useful queries
- Which atoms are grounded in `synthesis.md`?
- Which sources have no atoms yet?
- Which atoms are synthesized rather than directly grounded?

---

### FR-8: Machine-Readable Graph Contract
KGDB shall include source nodes and provenance edges in its graph snapshot outputs.

#### Required outputs
- graph snapshot with source nodes
- provenance edge data in node/edge structures
- preservation of source metadata and relation semantics

#### Required property
This information must be available in a machine-readable form suitable for downstream tools and audits.

---

### FR-9: Reflection Output Contract
KGDB reflection shall produce machine-readable findings relevant to provenance.

#### Required finding classes
- unknown source id
- orphan atom
- malformed provenance declaration
- unused source node
- synthesized claim with insufficient support (if rule enabled)

#### Output requirement
Findings shall be serializable in the existing or extended reflection output artifact format.

---

### FR-10: Backward-Compatible Degradation
KGDB should degrade safely when provenance data is absent.

#### Required behavior
- Existing graph functionality should continue working if source catalog or provenance blocks are not yet present.
- Missing provenance support should produce findings, not graph-construction failure, unless strict mode is explicitly enabled.

---

## 8. Data Contracts

### 8.1 Source Catalog Contract

#### File location
Recommended initial location:
- `desk/registry/source-catalog.yaml`

#### Contract
```yaml
sources:
  - id: source-doc-synthesis
    title: synthesis.md
    kind: project_doc
    family: project_documentation
    path: source_docs/Project_Documentation/synthesis.md
    stability: stable
    description: High-level synthesis of the ETM + ASI tutoring architecture.
```

#### Field semantics
- `id`: canonical source identifier used in provenance declarations
- `title`: human-readable name
- `kind`: source type classification
- `family`: source grouping for reflection and coverage
- `path`: repository path or declared source location
- `stability`: `stable` or `evolving`
- `description`: short semantic description

---

### 8.2 Atom Provenance Contract

#### Example
```yaml
provenance:
  - source_id: source-doc-synthesis
    relation: synthesized_from
    derivation: synthesis
    locator: "Sections 4-5"
    confidence: medium
    notes: Combines architectural synthesis with tutor design constraints.
```

#### Required fields
- `source_id`
- `relation`
- `derivation`

#### Optional fields
- `locator`
- `confidence`
- `notes`

#### Allowed `relation` values
- `supported_by`
- `synthesized_from`
- `design_derived_from`
- `about_dataset`

#### Allowed `derivation` values
Suggested set:
- `direct_quote`
- `paraphrase`
- `summary`
- `synthesis`
- `design_inference`

#### Suggested `confidence` values
- `high`
- `medium`
- `low`

---

### 8.3 Graph Node Contract for Source Nodes

Each source node should expose at least:
- `node_id`
- `node_type`
- `label`
- `path`
- `kind`
- `family`
- `stability`
- `description`

Example conceptual shape:
```json
{
  "identity": {
    "node_id": "source_doc:source-doc-synthesis",
    "node_type": "source_doc"
  },
  "semantics": {
    "label": "synthesis.md",
    "path": "source_docs/Project_Documentation/synthesis.md",
    "kind": "project_doc",
    "family": "project_documentation",
    "stability": "stable",
    "description": "High-level synthesis of the ETM + ASI tutoring architecture."
  }
}
```

---

### 8.4 Graph Edge Contract for Provenance Edges

Each provenance edge should expose at least:
- source node id
- target node id or equivalent directionality
- relation type
- derivation
- optional locator
- optional confidence

Example conceptual shape:
```json
{
  "from": "atom:atom-implicative-statistical-analysis-asi",
  "to": "source_doc:source-doc-manual-asi-estructurado",
  "relation": "supported_by",
  "derivation": "paraphrase",
  "locator": "Parte 1, secciones 1-3",
  "confidence": "high"
}
```

Directionality may be reversed if KGDB conventions require it, but the semantics must remain unambiguous.

---

## 9. Semantic Requirements

KGDB must preserve the meaning of provenance relations.

### `supported_by`
The atom is directly grounded in the source.

### `synthesized_from`
The atom combines multiple source-grounded components into a synthesized claim.

### `design_derived_from`
The atom represents a local design choice motivated by one or more sources.

### `about_dataset`
The atom describes the structure, location, or use of a dataset source.

KGDB must not collapse all provenance relations into a generic undifferentiated reference edge.

---

## 10. Validation and Reflection Requirements

### VR-1: Validate Source ID Resolution
Reflection must flag provenance entries whose `source_id` does not exist in the source catalog.

### VR-2: Validate Presence of Provenance
Reflection must flag atoms missing provenance declarations when provenance enforcement is enabled.

### VR-3: Validate Provenance Shape
Reflection must flag malformed provenance blocks, including:
- missing required fields
- unsupported relation values
- unsupported derivation values (if enumeration is enforced)

### VR-4: Validate Source Coverage
Reflection should flag source nodes with no atom support edges.

### VR-5: Validate Synthesis Support
If synthesis validation is enabled, reflection should flag `synthesized_from` atoms that declare only one source.

### VR-6: Produce Machine-Readable Findings
All provenance findings must be emitted in a structured format suitable for downstream inspection and CI automation.

---

## 11. Acceptance Criteria

The requirement set is satisfied when the following can be demonstrated in this repository.

### AC-1: Source Catalog Ingestion
Given a valid `desk/registry/source-catalog.yaml`, KGDB creates source nodes in the graph snapshot.

### AC-2: Provenance Edge Materialization
Given an atom with a valid provenance block referencing a known `source_id`, KGDB emits a typed provenance edge between the atom and the source node.

### AC-3: Unknown Source Detection
Given an atom referencing a nonexistent `source_id`, KGDB reflection emits an explicit unresolved-source finding.

### AC-4: Orphan Atom Detection
Given an atom with no provenance block, KGDB reflection flags it as orphan or unsupported.

### AC-5: Source Coverage Reporting
Given a source node unused by all atoms, KGDB reflection reports it as unused or uncovered.

### AC-6: Graph Queryability
The graph snapshot contains enough source-node and edge data to answer:
- which atoms come from a given source
- which atoms are synthesized
- which sources are unused

### AC-7: Backward-Compatible Operation
Existing graph build behavior still functions when provenance declarations are absent, unless explicit strict enforcement is enabled.

---

## 12. Examples from This Repository

### Example A: Direct Theory Grounding
Atom:
- `atom-implicative-statistical-analysis-asi`

Expected provenance:
- `source-doc-manual-asi-estructurado`
- optionally `source-doc-synthesis`

Expected relation:
- `supported_by` to the manual
- optionally `synthesized_from` if the atom combines multiple sources

### Example B: Design-Derived Pipeline Claim
Atom:
- `atom-the-two-step-evaluation-pipeline-architecture`

Expected provenance:
- `source-doc-synthesis`
- `source-doc-notas-de-tutor`

Expected relation:
- `design_derived_from` or `synthesized_from`

This atom should not be treated as if it were a direct source-grounded restatement of one single source.

### Example C: Dataset Location Atom
Atom:
- `atom-where-source-evaluations-are-located`

Expected provenance:
- `source-dir-evaluaciones-dama-ciclo-basico`

Expected relation:
- `about_dataset`

---

## 13. Implementation Notes

This document does not require a particular internal implementation, but the expected behavior implies the need for:

- a source-catalog extractor
- a provenance parser for atom metadata
- a provenance-edge builder
- provenance-aware reflection rules

Current local project artifacts already prepared for this direction include:
- `desk/registry/source-catalog.yaml`
- `desk/registry/kgdb-provenance-model.md`

---

## 14. Open Questions

1. Should provenance parsing be limited to atoms initially, or extended immediately to tasks and other desk artifacts?
2. Should strict enforcement be opt-in or default-on?
3. Should `confidence` remain free text or be enumerated?
4. Should locators support page numbers, headings, and arbitrary textual anchors?
5. Should KGDB create nodes only for catalog-declared sources, or also for auto-discovered external files?

---

## 15. Requested Outcome from KGDB Team

The requested outcome is not only a graph feature, but a stable contract for knowledge grounding.

The KGDB team is being asked to provide:

1. a supported source-node model
2. a supported provenance-edge model
3. graph snapshot inclusion of those semantics
4. reflection/validation for provenance integrity
5. enough stability that this can become part of the repository's ongoing knowledge-engineering workflow
