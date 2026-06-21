---
id: pill-orphans-and-gaps-are-reflection-findings
tags:
- workspace:desk
- artifact:pill
---

# Orphans and gaps are reflection findings

## What

_Define the context or guardrail this pill carries._

Missing provenance, unresolved source_id, malformed provenance blocks, and unused sources are first-class reflection findings with stable shape, never silent gaps or failures.

## Why

_Explain why this context matters for safe execution._

Silent gaps hide review debt. Without structured findings, downstream tools and humans cannot act on provenance problems; the substrate becomes unauditable.

## When

_Describe when an agent should apply this pill._

Designing or emitting any reflection rule; especially FR-5, FR-6, FR-7, and FR-9.

## Where

_Name the files, surfaces, or scope this pill applies to._

Reflection output artifact; the finding dataclass; tests that prove each finding class can be emitted and serialized.

## How

_Describe the correct way to apply this guidance._

Every absence or malformed-block is a finding with id, atom_id, source_id, relation, severity, message. Emit findings, never crashes; emit findings, never silent skips.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not raise an exception when provenance is absent; do not drop unknown source references; do not return success without surfacing the finding.
