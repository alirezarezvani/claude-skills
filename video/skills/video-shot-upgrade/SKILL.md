---
name: video-shot-upgrade
description: Use when turning approved animatic shots into AI-generated footage through the user's own video MCP (e.g. Higgsfield), or to price them first. Quotes each shot, needs a yes to the total, never resubmits a timeout, and checks plates against the animatic.
argument-hint: "[shots.json] [--adapter higgsfield] [--model id]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Adapter file per provider + model constraints read from the provider's catalog at run time → requests.v1; spend.v1 ledger as a state machine (quoted → approved → reserved → submitted → completed); ffmpeg frame comparison against animatic keyframes. Scripts call no service; the agent calls the MCP."
  distinct_from: "video-animatic (makes the free animatic and the shots.v1 manifest); cinematic-shot-prompting (writes a camera prompt for one clip, spends nothing); the provider's own server-side workflows (single clips, no gate tied to an approved cut)"
---

# Video Shot Upgrade

> **Portability:** Python stdlib + ffmpeg. Generation needs a video MCP the user connected, under their account and credits. Without one, the film ships as the motion-graphics cut and this skill is not needed.

Only for the `previz-to-final` lane, after the user approved the animatic.
Every credit passes three checks: a provider quote, the user's yes to that
exact total, and a reservation right before each generate call. A timed-out
call is never sent again on its own, because the provider may already have
charged it.

## Workflow

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills
# 0 shots.v1 from the approved scene, with clean keyframes from a --mode final page
python3 $S/video-animatic/scripts/frame_renderer.py --html film/final.html --out film/keyframes --keyframes
python3 $S/video-animatic/scripts/shot_manifest.py --scene film/scene.json --keyframes film/keyframes --out film/shots.json
# 1 model constraints come from the provider at run time (Higgsfield: models_explore action get), saved to a file
python3 $S/video-shot-upgrade/scripts/provider_adapter.py --shots film/shots.json --adapter higgsfield \
    --model <id> --model-spec film/model.json --out film/requests.json
# 2 upload keyframes (media_upload, PUT, media_confirm), put the ids in, call the quote tool per request,
#   save {"s2": {"credits": 15, "quote_ref": "quote:..."}} as film/quotes.json, read the balance
python3 $S/video-shot-upgrade/scripts/budget_gate.py quote --requests film/requests.json --quotes film/quotes.json \
    --brief film/brief.json --balance <credits> --ledger film/spend.json
# 3 show the per-shot table and the approval sentence; only after the user says it:
python3 $S/video-shot-upgrade/scripts/budget_gate.py approve --ledger film/spend.json --credits <total> --said "<their words>"
# 4 per shot: reserve, generate once, record
python3 $S/video-shot-upgrade/scripts/budget_gate.py reserve --ledger film/spend.json --shot s2
#   generate_video with params {"ref": "<quote_ref>"}  →  job id
python3 $S/video-shot-upgrade/scripts/budget_gate.py record --ledger film/spend.json --shot s2 --job-id <id> --status submitted
#   jobs_wait until terminal; download to film/plates/s2.mp4
python3 $S/video-shot-upgrade/scripts/budget_gate.py record --ledger film/spend.json --shot s2 --status completed --plate film/plates/s2.mp4
# 5 does the plate keep the animatic's framing? writes a final scene with the plates that hold
python3 $S/video-shot-upgrade/scripts/drift_check.py --requests film/requests.json --shots film/shots.json \
    --plates film/plates --scene film/scene.json --scene-out film/scene.final.json
```

Then hand `scene.final.json` back to `video-animatic` (`--mode final`) and
`video-conform`. Text, charts and logos stay as code layers over the plate.

## Exit codes

| Script | 0 | 3 | 4 |
|---|---|---|---|
| `provider_adapter.py` | requests written | no `--model-spec`: it prints the catalog call to make | a shot the model cannot make (aspect, too long, empty prompt) |
| `budget_gate.py` | step recorded | quotes or ledger missing | over cap, over balance, wrong total, stale quote, second call for one shot |
| `drift_check.py` | every plate holds | a human must look (REVIEW), or no ffmpeg | a plate drifted: re-prompt or keep the shot as motion graphics |

## Rules that come from the providers

- Read tool names and model constraints at run time. Adapters name tool roles
  (quote, generate, wait, upload); match them against the tools you have by
  suffix, and stop if one is missing rather than guessing a substitute.
- Higgsfield (verified 2026-11-26): quote with `estimate_video_cost`;
  `generate_video` no longer takes `get_cost`. Generate with
  `params: {"ref": "<quote_ref>"}` so exactly the quoted request runs. Never
  set `use_unlim`; an `unlim_choice` reply means nothing was submitted and the
  question goes to the user. Media take ids from `media_upload` +
  `media_confirm`, never local paths.
- Plates are generated silent (the adapter sets the model's audio switch off);
  voice-over and music are mixed in conform.
- A model with a 4 s minimum makes a 2.5 s shot cost 4 s. The adapter reports
  the paid-and-trimmed seconds; say them in the quote.

## Hard rules

- No quote call before the animatic is approved; no generate call without an
  approved ledger and a fresh `reserve`.
- One quote buys one call. A failed shot needs `record --release-failed`, which
  is a new yes from the user, and a new quote if the old one aged out.
- Real-person likeness needs recorded consent (the brief gate refuses without
  it). Label generated footage as AI-generated where it is published.
- What leaves the machine: prompt, duration, aspect and keyframe stills, to the
  user's provider only.

## Forcing-question library

1. **Which shots earn generated footage?** Recommended: one hero shot first; the rest stay motion graphics until it holds.
2. **What is the credit cap for this batch?** Recommended: the quoted total of that one shot plus nothing; raise it only after drift_check passes.
3. **Which model?** Recommended: the provider's default for image-to-video that accepts both start and end keyframes in the scene's aspect.
4. **What happens if the plate drifts?** Recommended: keep the motion-graphics shot; one re-prompt at most, quoted again.

## References

- [provider_adapters.md](references/provider_adapters.md) — adapter format, how to add a provider, why each gate exists, drift thresholds
- Adapters: `adapters/higgsfield.json`, `adapters/template.json`
- Sibling skills: `video-director`, `video-animatic`, `video-conform`
