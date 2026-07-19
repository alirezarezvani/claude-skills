---
name: fable-goal
description: Convert a rambling description of a desired outcome into one polished, autonomous /goal prompt ready to paste into a fresh session. Use when the user says "/fable-goal", "turn this into a goal prompt", "write me a fable prompt", "write the prompt that builds X", or rambles about something they want made and asks for the prompt that makes it happen. The output is a single copy-paste prompt, never the build itself. Do NOT use when the user wants the thing built right now in this session — only when they want the PROMPT that will make it happen in a fresh session.
---

# Fable Goal Prompt Writer

Turn the user's ramble into one exceptional /goal prompt they can paste into a fresh autonomous session. You are not building the thing. You are designing the prompt that builds the thing.

**Wrong-tool check first.** If the user actually wants the deliverable built now, say so in one line and offer to build it — don't write a prompt nobody will paste.

## The philosophy

**Get out of the model's way.** A capable model can do almost anything if the prompt (1) articulates the desire clearly, (2) hands it tools, and (3) gives it a way to verify its own work. A great /goal prompt does not micromanage the how. It nails the *what*, grants explicit creative freedom on execution, and demands self-verification before done.

The corollary most prompts miss: **done must be observable.** Every deliverable needs a completion condition the session can check itself — a page that loads, a script that runs on real input, a link that resolves. "Make it good" is a wish; "load each page and click every element before you ok it" is a verification loop.

**Brand profile (optional).** If the user keeps one — a `brand.md` in this folder, or `~/.claude/CLAUDE.md` / `~/.claude/brand-profile.md` — read it once at the start: proof points, audience numbers, design system, asset paths, default destinations, voice rules, preferred MCPs. Pull in ONLY entries the task touches. No profile is fine; a profile just removes questions.

## Process

### 1. Extract what the ramble already contains

People think in fragments, especially over voice-to-text. Interpret intent over literal words ("Quad MD" means CLAUDE.md, "Netlefi" means Netlify). Pull out six slots: **deliverable** (the concrete thing), **quantity**, **audience/stakes** (who sees it, real numbers), **tools named**, **quality bar** (adjectives, comparisons), **destination** (hosted link, folder, post, file).

### 2. Fill gaps with defaults; ask only when it matters

Synthesize small gaps yourself, using the brand profile if one exists. Ask ONLY when the answer would meaningfully change the prompt: **outcome** (can't tell what the deliverable is), **scale** (5 vs 50 changes the shape and nothing implies it), **destination** (can't infer where results land), **assets** (a needed input like a logo or source file that nothing supplies), **brand facts** (public-facing output with no profile — ask for the one or two that raise the bar).

If you ask, ask everything in ONE AskUserQuestion batch, then write. Never interview in rounds. If the ramble (plus profile) covers the basics, ask nothing and note assumptions instead.

### 3. Verify before you name

A prompt that points at a path, capability, or MCP that does not exist sends the fresh session on a dead-end hunt. Spend 30 seconds confirming every resource you plan to name: `ls` the paths, glance at the available-tools list. The live environment is the source of truth, not the profile. Name only what you verified AND what is load-bearing (usually 2–4 things); everything else is the discovery mandate's job.

### 4. Write the prompt: the seven-part anatomy

Weave all seven parts as natural flowing prose — no headers, no bulleted spec. First person, as the user speaking to the session:

1. **Desire + stakes.** Concrete deliverable, concrete quantity, why it matters. If an audience will see it, say so with the real number. Never invent stakes — real stakes make the model try harder; fake ones are noise.
2. **Quality bar.** What excellent looks like, in a sentence or two. For creative work, vivid adjectives beat specs; for functional work, concrete behavior beats adjectives.
3. **Tool inventory + discovery mandate.** Name the verified resources, sketch ONE example workflow as a suggestion, then release it: "you can accomplish this many ways." Then grant discovery — "before you start, take stock of the tools and MCPs you actually have, and go find or fetch any references, libraries, or assets you need along the way; the internet is available to you."
4. **Creative freedom + decision authority.** Explicit permission to deviate, choose workflows, and "show what you're capable of." Never skip this. Anything named is a suggestion the session may swap for something better; every mid-run judgment call gets decided by the session with taste, not deferred back.
5. **Verification loop.** Default: at least three iteration passes — going back through the finished output with a fine-toothed comb for problems and improvements. Define the pass in the medium's own terms: load the page and click through it, run the script on real input, render and watch the video. See [references/goal_prompt_patterns.md](references/goal_prompt_patterns.md) for per-medium defaults.
6. **Delivery.** Exactly where results land and what gets served back: the link, the file path, the post URL.
7. **Goal line + autonomy directive.** Close with one sentence: "[X with Y and Z] is your /goal. Work completely autonomously and do not ask me for anything until you are all done." For 3+ independent units, add a nudge to parallelize with subagents.

**Length target: 150–350 words** — long enough for stakes, tools, and verification; short enough that nothing dilutes the goal line.

### 5. Self-check, then deliver

Fix any miss before shipping: (1) deliverable + quantity concrete enough that a stranger could judge done; (2) every named resource verified in step 3; (3) creative-freedom clause present; (4) verification loop present and matched to the medium; (5) destination explicit; (6) ends with the goal line + autonomy directive, 150–350 words.

The mechanically checkable subset (word count, goal line, autonomy directive, verification/freedom/destination language) can be run: `python3 scripts/goal_prompt_self_check.py -` with the draft on stdin — exit 0 means those checks pass; judgment calls (1) and (2) stay yours.

Output the prompt in a single fenced code block, then a short **Assumptions** list (2–4 bullets) so the user can correct any gap-fill with one line. Nothing else — no preamble above the code block.

## Anti-patterns

Never ship a prompt that: **micromanages the how** (step-by-step strangles the session); **names phantom resources** (unverified = dead-end hunt); **has unverifiable done-ness** (session declares victory early); **buries the goal line** (nothing comes after it); **invents stakes** (false urgency trains the user to write fiction); or follows an **interview spiral** (one question batch max). Failure-mode detail and a second worked example (non-web medium) live in [references/goal_prompt_patterns.md](references/goal_prompt_patterns.md).

## Example

**Ramble:** "I want like 5 different landing pages for my free prompt pack thing, they should all look totally different and crazy good, put them up somewhere I can look at them"

**Output:**

```
I want you to build 5 landing pages for my free prompt pack, each one fundamentally different from the others, as a way to show me the strongest possible range of directions before I pick one. These will be seen by my audience, so the bar is high: exceptional typography, striking layouts, and motion that feels designed rather than templated. Each page needs a headline, proof, and a single email-capture CTA for the prompt pack. You have total creative freedom on the visual direction of each one. You can generate any imagery you need with whatever image tools you have available, and you can accomplish this in many ways using many workflows, so before you start, take stock of the tools and MCPs you actually have, go find or fetch any references, libraries, or assets you need along the way, and show me what you are capable of. Before you ok each page, do at least three iteration passes: load the live page, click through every element, check it at mobile width, and go back through with a fine-toothed comb looking for design problems and opportunities to improve. Parallelize across subagents so the pages develop independently. When all 5 are done, deploy them to Netlify and serve me the 5 links with a one-line description of each direction. 5 fundamentally different prompt pack landing pages, live on Netlify with three iteration passes each, is your /goal. Work completely autonomously and do not ask me for anything until you are all done.
```

**Assumptions:**
- CTA is email capture for the prompt pack (review candidates, not live pages — no marketing-automation wiring)
- Netlify for hosting since you said "put them up somewhere"
- Each page gets a distinct visual direction so you see the full range before committing

---

*Derived from [duncan-buildroom/freeskills](https://github.com/duncan-buildroom/freeskills) `fable-goal` ("free to use and modify"). Substantially restructured: wrong-tool check, observable-done principle, six-slot extraction, per-medium verification defaults, six-point self-check, anti-pattern list, second worked example.*
