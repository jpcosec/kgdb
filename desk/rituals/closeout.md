# Closeout ritual

Close a kgdb task in 6 ordered steps. Each step must succeed before the next begins.

## Steps

### 1. Validate

Run the concrete validation checks listed in the task's **Validation** section. If the task has no validation section, add one before closing. Use the [testing ritual](testing.md): start with the smallest relevant check, then broaden.

### 2. Graduate pills to stable knowledge

If this task consumed or created a **pill** (a reusable context document in `desk/contexts/` or `desk/pills/`), the pill's knowledge must be absorbed into stable project docs before closeout:

- **Contracts, schemas, formats** → `contracts/` or `docs/`
- **CLI behavior, conventions** → `README.md` or `docs/`
- **Architecture decisions** → `docs/adr/` or `atom-kgdb.md`

Delete the pill file after its knowledge is absorbed. Pills are transient; they should not accumulate.

### 3. Delete the task file

Do not mark `status: closed`. Delete the file. If the task has dependency tasks that are now also complete (e.g. a prerequisite that has no further use), delete those too.

### 4. Update the Board

In `Board.md`:

- Remove the deleted task's row from the **Active** table.
- If the deletion unblocks a dependent task, move that task from **Blocked** to **Active**.
- If this completes a Phase, note it in the header summary.

### 5. Update the atom (if needed)

If the task changed kgdb's contracts, capabilities, or status, update `desk/atoms/atom-kgdb.md` — keep the atom truthful.

### 6. Commit

Stage only the intended files:

1. The deleted task file(s) — visible as deletions.
2. `Board.md`.
3. Any implementation files added or changed.
4. Any stable-docs changes from step 2.
5. Atom changes.
6. Update `changelog.md` with a line per deleted task.

Write a commit message in the style:

```
ritual: close task kgdb/<n> - <task-title>

<bullet list of what changed>
```

Do not amend or force-push. Do not commit unless explicitly told to.

### 7. Reflect

After closeout, pause before picking up the next task:

- Is there anything that should go into the **drawer** (deferred / not-yet-actionable)?
- Is there anything that should be filed in the **inbox** (suggestion, observation, deskops signal)?
- Is any other open task now blocked, unblocked, or re-prioritizable?

No task is closed until the commit lands and the board is clean.

---

## Deskops integration

kgdb receives suggestions and signals from `deskops` via the inbox (`desk/inbox/`). During closeout, check whether any deskops signal relates to the task being closed — if so, reply or close the loop before deleting.

When pills reference deskops-specific concepts (lifecycle gates, atom docs, source URIs), those graduate into `contracts/` or `docs/`, not into kgdb's own source code. kgdb stays substrate-dumb; deskops-specific logic lives in deskops adapter code.
