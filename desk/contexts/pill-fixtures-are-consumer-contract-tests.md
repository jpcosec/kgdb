---
id: pill-fixtures-are-consumer-contract-tests
tags:
- workspace:desk
- artifact:pill
---

# Fixtures are consumer-contract tests

## What

_Define the context or guardrail this pill carries._

A fixture in desk/fixtures/ is not just sample data; it is a contract test. It proves a real downstream consumer can read the substrate's output shape.

## Why

_Explain why this context matters for safe execution._

Without fixtures, the consumer-contract shape is theoretical. With fixtures, every change to the IO contract that breaks a consumer fails CI immediately.

## When

_Describe when an agent should apply this pill._

Authoring or modifying a fixture; updating the IO contract; running integration tests.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task-create-substrate-fixture, task-prove-downstream-consumer-contract, and the SL-3 cross-repo roundtrip test.

## How

_Describe the correct way to apply this guidance._

Treat fixtures as tests: load them, validate against the contract, hand them to a stub consumer, assert the expected consumer-facing shape. Never skip them in CI.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not keep stale fixtures that don't match the current contract; do not let fixtures drift from the consumer shape they were authored to prove.
