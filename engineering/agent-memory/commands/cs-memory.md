---
description: Inspect, trace, and adopt the tiered agent-memory store (status | why | contested | adopt | forget)
argument-hint: "status | why \"<claim>\" | contested | adopt | forget \"<claim>\""
---

# /cs:memory — curate what the agent remembers

Argument: `$ARGUMENTS` (default: `status`)

Scripts live at
`engineering/agent-memory/skills/agent-memory/scripts/`. All are stdlib-only and
read-only except where stated.

---

## `status` (default)

1. Run `memory_inspect.py --tier L3`, `--tier L2`, `--tier L1`.
2. Read `.memory/staged/promotions.json` if it exists.
3. Read the last 7 days of `.memory/errors.log` if it exists — **surface any
   entry**. That file is where silently dropped writes are recorded, and a log
   nobody is pointed at is the same as no log.

Report, in this order: what is always loaded (L3), what this project loads (L2),
how many candidates are waiting and what is blocking each, what is staged for
adoption, and any dropped writes.

**Do not adopt anything here.** `status` is read-only.

---

## `why "<claim>"`

Run `memory_inspect.py --why "<claim>"`.

Report the full provenance: observation count, distinct sessions, distinct
calendar days, first and latest transcript back-pointers, whether each resolves,
and the quoted source line when exactly one transcript matched.

If the resolution status is **`ambiguous`**, say so plainly and print no source
line. Two projects can hold a transcript of the same basename; guessing attaches
a real claim to the wrong session, and a wrong citation is worse than none.

---

## `contested`

Run `memory_inspect.py --contested`.

For each pair, present both claims with their dates and sources side by side and
ask the user which governs. **Do not pick.** Do not merge them. Do not mark one
resolved on your own judgement — resolution is a human decision by design.

---

## `adopt`

The only command in this file that writes. Six steps, in order, no skipping:

1. Run `memory_promote.py --stage` to refresh `.memory/staged/promotions.json`.
2. **Back up both `CLAUDE.md` files** (project and global) with a timestamped
   copy. Do this before writing anything, every time.
3. Walk the staged list **one atom at a time**. For each, show the claim, the
   evidence (sessions, days, sources), and the target file. Wait for the user.
4. **Refuse outright** any atom with `redacted: true` — no amount of evidence
   substitutes for the human reading the original. Explain why and move on.
5. **Refuse** any atom whose citation does not resolve.
6. Append accepted atoms to the target `CLAUDE.md` under a clearly marked
   `<!-- agent-memory: adopted -->` section, and log each to `.memory/adopted.log`.

Never write to a `CLAUDE.md` outside this flow. Never batch-accept.

---

## `forget "<claim>"`

1. Locate the atom with `memory_inspect.py --why "<claim>"`.
2. Show the user exactly what will be removed, from which tier, and whether it
   was already adopted into a `CLAUDE.md`.
3. On confirmation, remove it from `.memory/atoms.jsonl` and, if it was adopted,
   remove the corresponding line from the `CLAUDE.md` — after backing that file
   up.

Removing an atom does **not** prevent re-learning. If the marker fires again in
a future session, it returns. That is correct: forgetting is not a permanent
veto, and saying so avoids a confusing surprise later. To stop it returning,
change the underlying fact or state the correction — a correction is itself a
high-confidence observation.

---

## Refuse and route

- No `.memory/` directory yet → say so. It is created on the first session end
  with the hooks installed; nothing is wrong.
- User asks to lower a promotion threshold so something passes → refuse. Gates
  are changed in the open, in `DESIGN.md`, not per-claim. Offer to record the
  case as evidence the threshold is wrong.
- User asks to design or price a memory system generally → route to
  `engineering/memory-engineering`. This skill *is* a memory system; that one
  audits any of them, this one included.
