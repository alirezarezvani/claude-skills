# Memory Control and Governance — who controls what it keeps

> The Anthropic lens: *who controls what it keeps?*
>
> Every figure is attributed with a confidence level. The customer metrics in
> §4 are **vendor-published testimonials**, not controlled studies, and are
> labeled as such.

---

## 1. A wrong memory does not fail once

This is the asymmetry that makes memory governance different from ordinary
storage governance:

**A bad retrieval fails one query. A bad memory fails every future session that
reads it.**

An error written into memory is not a transient defect — it is a persistent
one that compounds, propagates into derived records during consolidation, and
is retrieved with the same confidence as a correct one. By the time you notice,
it has been read hundreds of times and possibly rewritten into summaries.

This is why control is not a layer added on top of a memory system. It is a
property the system either has by construction or does not have at all.

## 2. Memory as files — the deliberately boring move

Anthropic's design for Claude Managed Agents mounts memory as **files on a
filesystem**, at `/mnt/memory/` inside the agent's container, so the agent reads
and writes memory with the same bash and code-execution tools it already uses.

> Memory is "a workspace-scoped collection of text documents mounted as a
> directory," relying on "the same bash and code execution capabilities that
> make it effective at agentic tasks."
> — Anthropic, *Built-in memory for Claude Managed Agents*
> (confidence: **high**)

The choice looks unambitious, and that is the argument for it. Files give you,
for free, every property a bespoke store has to reimplement:

| Property | What files give you |
|---|---|
| Inspection | `cat`, `grep`, a text editor |
| Diffing | `diff`, version control |
| Export | copy the directory |
| Selective deletion | `rm` one file |
| Programmatic control | any language's file API |
| Review | a human reads it without a query language |

**The test:** *a store you cannot open and edit is a store you do not control.*
If answering "what does the agent believe about X, and why?" requires writing a
query against an embedding index, you have given up observability to gain
retrieval convenience.

## 3. Scope, audit, rollback

The three controls, as implemented in the Anthropic design (confidence:
**high** — all quoted from vendor documentation):

**Scope.** Access is set per store: `read_only` makes the mount read-only at
the filesystem level; `read_write` allows create, edit, and delete. An org-wide
store is typically read-only while per-user stores are writable — so shared
knowledge cannot be corrupted by one agent's bad session. Multiple agents can
work concurrently against the same store without overwriting each other.

**Audit.** "Each write becomes a session event with a timestamp, source
attribution, and a rollback option." Session events surface in the Console.
This is what makes a wrong memory traceable to the session that wrote it —
without attribution, you can detect a bad fact but not find its origin, which
means you cannot stop it recurring.

**Rollback.** Earlier versions can be restored, and content can be redacted
from history. Note the second half: *redaction from history* is a distinct
capability from *restoring a prior version*, and regimes like GDPR's right to
erasure require the former.

These map to checks **F5** (scope), **F6** (audit trail), and **F7** (rollback)
in `forgetting_policy_linter.py`.

## 4. Reported outcomes — read the label

Vendor-published customer testimonials accompanying the Anthropic memory
launch:

| Source | Reported result |
|---|---|
| Rakuten (Yusuke Kaji, GM AI for Business) | "97% fewer first-pass errors" at "27% lower cost and 34% lower latency" |
| Wisedocs (Denys Linkov, Head of ML) | Memory use "sped verification up 30%" |

**Confidence: low-to-moderate, and the reason matters.** These are named,
attributable, on-the-record customer statements — which is better than an
anonymous benchmark — but they are:

- **not controlled experiments** (no stated baseline methodology, no control arm);
- **selected for publication** by the vendor;
- **not isolated to memory** (a team that adds memory usually changes other
  things at the same time).

⚠️ A widely-shared summary of this material presents the 97% figure as though it
were a general property of building memory this way — "teams building this way
cut first-pass errors by 97 percent." That overstates it. It is *one named
customer's reported result*, not a generalizable finding. Cite it as Rakuten's
claim, with the attribution attached, or do not cite it.

The defensible version of the claim is the mechanism, not the number:
**observable learning is debuggable learning.** When every write is attributed
and reversible, you can find and fix a bad memory instead of discovering it as
unexplained model drift.

## 5. Memory poisoning is a security boundary, not just a quality problem

If an agent writes to memory based on content it reads, then **anything that
can influence what the agent reads can influence what it permanently believes.**
A prompt injection that lands in a memory record does not end with the session
— it persists and is retrieved as trusted context later.

Minimum controls:

1. **Separate write authority from read exposure.** The component that ingests
   untrusted content should not be the component with write scope.
2. **Attribute every write to a source**, so injected records can be traced and
   swept.
3. **Keep the delete path fast.** Incident response on a poisoned memory store
   is bounded by how quickly you can remove records.
4. **Treat consolidation as an amplifier.** A merge pass propagates a poisoned
   record into derived records, past the point where source attribution helps.

## 6. The governance checklist

Before a memory system holds anything that matters:

- [ ] Read scope and write scope are both named, and they differ
- [ ] Every write carries a timestamp and a source
- [ ] There is a restore path *and* a hard-delete path
- [ ] Deletion satisfies your regulatory obligations (erasure, not just tombstoning)
- [ ] A human can read the store without a query language
- [ ] Untrusted-content ingestion does not hold write scope
- [ ] Contradictions surface to a human rather than resolving silently

---

## Sources

1. Anthropic — *Built-in memory for Claude Managed Agents*.
   <https://claude.com/blog/claude-managed-agents-memory> — primary source for
   §2, §3, §4.
2. `anthropics/skills` — `skills/claude-api/shared/managed-agents-memory.md`.
   Implementation-level reference for scopes and store semantics.
   <https://github.com/anthropics/skills>
3. Anthropic — memory tool documentation, Claude Developer Platform. Reference
   for the filesystem-backed memory tool surface.
4. OWASP — *Top 10 for LLM Applications*, notably LLM01 (Prompt Injection) and
   the agentic-memory poisoning discussion. Basis for §5.
5. NIST — *AI Risk Management Framework* (AI 100-1), MAP and MEASURE functions.
   Governance framing for auditability requirements.
6. Regulation (EU) 2016/679 (GDPR), Article 17 — right to erasure. Why redaction
   from history is a distinct requirement from version rollback.
7. Anthropic — *Building effective agents* (2024). Design context for
   tool-mediated agent state.

## Related tools in this skill

- `forgetting_policy_linter.py` — §3 (F5 scope, F6 audit, F7 rollback),
  §6 (F4 contradictions)
