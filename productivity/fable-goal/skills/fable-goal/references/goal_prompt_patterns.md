# Goal Prompt Patterns — why the anatomy works

Supporting rationale for the seven-part anatomy in SKILL.md, plus the failure-mode catalog in long form. Read this when adapting the skill to a new medium or when a generated prompt underperforms.

## Why each part exists

**1. Desire + stakes.** Autonomous sessions calibrate effort to perceived importance. A deliverable with a named audience and a real number ("my 40k newsletter subscribers will see this") measurably shifts output quality versus "make me a page." The constraint: stakes must be true. A user who learns to invent audience numbers to juice quality is being trained to lie to their own tools, and the model eventually calibrates to the inflation.

**2. Quality bar.** Adjectives outperform specs for creative work because specs anchor the model to a checklist floor while adjectives set a ceiling to reach for. "Otherworldly beautiful animations" produces more ambitious work than "use CSS transitions of at least 300ms." For non-creative work (a CLI, a pipeline), invert this: concrete behavior beats adjectives ("a dry-run mode that shows me what it would do" > "make it safe").

**3. Tool inventory + discovery mandate.** Two failure modes bracket this part. Naming too much: every named tool is an implicit instruction, and ten named tools reads as a workflow spec — the thing the philosophy says not to write. Naming nothing: the session works from memory, guesses at what exists, and stops short when it hits a gap. The fix is 2–4 verified, load-bearing names plus one sentence of discovery mandate. The discovery sentence matters more than the inventory: it converts "I don't have X" from a stopping condition into a search task.

**4. Creative freedom + decision authority.** Without an explicit grant, capable models default to conservative interpretation and mid-run check-ins — both poison for an autonomous run. The grant has two halves that are easy to conflate: *creative* freedom (visual/structural choices) and *decision* authority (judgment calls like naming, scope edges, tradeoffs get made, not deferred). A prompt can grant the first and still get a session that stops to ask about the second.

**5. Verification loop.** The single highest-leverage part. An autonomous session with no self-check declares victory at first plausible output. "Three iteration passes" works because it is countable — the session can verify its own compliance — and because pass 1 catches errors, pass 2 catches what pass 1's fixes broke, and pass 3 is where polish happens. The pass must be defined in the medium's own terms (load the page, run the script, watch the render); "review your work" without a medium-specific action degrades into re-reading the code.

**6. Delivery.** Ambiguous destinations produce orphaned work: builds that finish in a scratch directory nobody looks at. Naming the destination also names the hand-back artifact (the link, the path), which becomes part of the observable done condition.

**7. Goal line + autonomy directive.** Restating the deliverable as the final sentence exploits recency: it is the last thing in context before the session begins, and it survives context compression in long runs better than a spec buried mid-prompt. The autonomy directive ("do not ask me for anything until you are all done") is load-bearing — without it, sessions surface questions the prompt already answered.

## Failure-mode catalog

| Failure | Symptom in the fresh session | Root cause in the prompt |
|---------|------------------------------|--------------------------|
| Micromanaged how | Mechanical, joyless output; session ignores better paths it noticed | Step-by-step instructions instead of outcome + freedom |
| Phantom resources | Session burns early turns hunting a path/MCP that doesn't exist, sometimes hallucinating around it | Named resource never verified against the live environment |
| Unverifiable done | Session ships first plausible draft; quality lottery | No observable completion condition, no defined pass |
| Buried goal line | Session over-weights a mid-prompt detail, under-delivers the actual goal | Closing sentence isn't the deliverable restated; content after the goal line |
| Invented stakes | Short-term quality bump, long-term calibration rot | Fake audience numbers or false urgency |
| Interview spiral | User abandons the skill; ramble-to-prompt loses its speed advantage | Multi-round questioning instead of one batch + assumptions |
| Scope creep grant | Session builds adjacent things the user never asked for | Freedom clause written without a concrete deliverable to bound it |

The last row is the counterweight to part 4: creative freedom is safe only when part 1 nailed the *what*. Freedom without a concrete deliverable is a scope-creep license.

## Verification defaults by medium

| Medium | The pass is… |
|--------|--------------|
| Web page / app | Load the live page, click every element, check mobile width |
| Script / CLI / automation | Run it on real input end to end; feed it a bad input too |
| Video / animation | Render and watch the whole thing at full speed |
| Written content | Read it aloud pass; check every claim and link |
| Data pipeline / analysis | Run on a real sample; sanity-check the numbers against a known figure |
| Design / image assets | View at actual size and in context, not just the editor |

For anything else, derive the pass from one question: **what would the end user do with this on day one?** The pass is the session doing exactly that. A Slack bot's pass is messaging it. A spreadsheet template's pass is filling it in with real-ish data. An API's pass is calling every endpoint including with malformed input. If you cannot phrase the pass as an action on the finished artifact, the deliverable is not concrete enough yet — go back to part 1.

## Worked example: a non-web medium

**Ramble:** "ugh I keep manually renaming and sorting all the podcast episode files my editor sends me, can you write me a prompt so fable just builds me something for that"

**Output:**

```
I want you to build me a small command-line tool that takes a folder of podcast episode files from my editor and renames and sorts them into my archive automatically, because I currently lose time every week doing this by hand. The tool should figure out the episode number and title from the messy filenames my editor uses, rename each file to a clean consistent pattern, and move it into a per-season folder structure, with a dry-run mode that shows me what it would do before touching anything. You have full freedom on language, structure, and approach — pick whatever makes this most robust and easiest for me to run, and take stock of the tools you actually have before you start, fetching any libraries you need along the way. Before you call it done, do at least three iteration passes: run it end to end on a realistic set of sample files you generate yourself, including at least a few badly named ones and one duplicate, and make sure the dry-run output is honest about what the real run will do. When it works, put the tool and a short README with the exact command I run in a folder called podcast-sorter in my home directory, and show me the dry-run output from your final test. A working, tested podcast file renaming and sorting CLI with dry-run mode, in ~/podcast-sorter with a README, is your /goal. Work completely autonomously and do not ask me for anything until you are all done.
```

**Assumptions:**
- Local CLI in your home directory since you didn't name a destination
- Dry-run mode included because the tool moves your real files
- The session generates its own realistic test fixtures since you didn't provide sample filenames

Note how the quality bar inverted for functional work (concrete behavior — dry-run mode, duplicate handling — instead of adjectives) and the verification pass matched the medium (run end to end on generated fixtures, including bad input).

## Sources

- Duncan / buildroom, [`freeskills/fable-goal`](https://github.com/duncan-buildroom/freeskills) — the upstream skill and the "25 websites" reference example that defines the genre
- Anthropic, [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) — verification loops and target-based iteration for agentic runs
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — observable completion conditions; why sessions need self-checkable done states
- Anthropic, [Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — clarity of desired outcome over prescriptive process
- This repo's `engineering/agent-harness` references — verifier's law: work you can verify mechanically gets done reliably; work you can't, doesn't
