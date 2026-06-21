---
id: pill-closed-tasks-are-deleted-not-marked
tags:
- workspace:desk
- artifact:pill
---

# Closed tasks are deleted, not marked

## What

_Define the context or guardrail this pill carries._

When a task closes, its file and its deskops artifacts are removed from disk. Closed tasks do not accumulate as status: closed files in the desk.

## Why

_Explain why this context matters for safe execution._

Closed files rot. They reference pills that may have changed, depend on tasks that no longer exist, and confuse routing. The desk must reflect current state only.

## When

_Describe when an agent should apply this pill._

Running the closeout ritual; finishing the final checklist of any task.

## Where

_Name the files, surfaces, or scope this pill applies to._

desk/rituals/closeout.md; the routine graph's close-to-complete edge; the closeout checklist.

## How

_Describe the correct way to apply this guidance._

Follow desk/rituals/closeout.md end to end. Delete the task file, routine file, checklists, operators, and edges. Update Board.md, changelog, and commit.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not mark status: closed and leave the file; do not keep closed tasks for history; do not skip the changelog or commit steps.
