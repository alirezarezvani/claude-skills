# Provider adapters, the spend gate and drift checks

## Why the adapter is a data file

Generation MCPs change faster than a plugin release. Between 2026-11-17 and
2026-11-26 Higgsfield moved price quotes out of `generate_video` (which used to
take `get_cost: true`) into a separate `estimate_video_cost` tool. A skill that
hard-coded the old call would have started paid jobs while trying to quote.

So the plugin splits what changes at different speeds:

| Changes | Where it lives | Who reads it |
|---|---|---|
| Tool roles and parameter names (months) | `adapters/<provider>.json` | `provider_adapter.py`, the agent |
| Models, durations, aspects (weeks) | the provider's catalog, read at run time and saved as `--model-spec` | `provider_adapter.py` |
| Prices (hours) | the provider's quote tool, called per request | `budget_gate.py quote` |

## adapter.v1

```json
{"schema": "adapter.v1", "provider": "higgsfield", "verified_on": "2026-11-26",
 "tools": {"catalog": "models_explore", "quote": "estimate_video_cost", "generate": "generate_video",
           "wait": "jobs_wait", "upload": "media_upload", "confirm_upload": "media_confirm", "balance": "balance"},
 "tool_match": "suffix",
 "params": {"model": "model", "prompt": "prompt", "duration": "duration", "aspect_ratio": "aspect_ratio",
            "media_list": "medias", "media_role_start": "start_image", "media_role_end": "end_image",
            "silent": [{"name": "generate_audio", "value": false}]},
 "generate_from_quote": {"params": {"ref": "<quote_ref>"}},
 "rules": ["..."], "data_flow": "..."}
```

`tool_match: suffix` means the agent looks for a tool whose name ends in the
role's value (`mcp__Higgsfield__estimate_video_cost`), because the server
prefix depends on how the user named the connector.

### Adding a provider

1. Copy `adapters/template.json` to `adapters/<provider>.json`.
2. Read the provider's live tool list. Fill each role or leave it `null`.
3. If the provider has no price preflight, leave `quote` null. `budget_gate.py`
   still needs a price per shot in `quotes.json`; it then comes from the
   provider's published price list, and you tell the user it is an estimate
   you could not confirm.
4. Write `verified_on` and `verified_how`. Call only tools that spend nothing
   while verifying (catalog, quote, balance).
5. Run `provider_adapter.py --adapter <provider> --sample` style checks with a
   saved model spec before anyone spends.

## Exit codes

| Script | 0 | 3 | 4 |
|---|---|---|---|
| `provider_adapter.py` | requests written | no `--model-spec`: it prints the catalog call to make | a shot the model cannot make (aspect, too long, empty prompt) |
| `budget_gate.py` | step recorded | quotes or ledger missing, ledger locked | over cap, over balance, wrong total, stale quote or yes, second call for one shot, re-quoting a live batch |
| `drift_check.py` | every plate holds | a human must look (REVIEW), or no ffmpeg | a plate drifted: re-prompt or keep the shot as motion graphics |

## Provider rules

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

## Why each gate exists

| Gate | Failure it prevents |
|---|---|
| Cap is the lower of `budget_credits` and `--cap` | a capped test silently inheriting the film's whole budget |
| Balance check | a batch half-submitted when credits run out, leaving a film with a hole |
| Approval must equal the quoted total | a yes to "about 20" being stretched over a 28-credit batch |
| Quotes expire (60 min default) | approving yesterday's price |
| `reserve` before every generate call | two calls for one shot after a resumed or compacted session |
| `unknown` state is terminal for retries | a timeout that was charged being paid twice; Higgsfield's own tool text says a timed-out submission may exist |
| `--release-failed` | a failed job retried without a second yes |

## Drift thresholds

`drift_check.py` downsamples the plate's first and last frames and the
animatic keyframes to 32x32, then averages two Pearson correlations: luma
(where light and dark sit) and a gradient map (where edges sit). This is a
cheap cousin of SSIM's structure term (Wang et al., 2004) without the window
machinery, enough to say "the composition moved" and stdlib-only.

| Measure | HOLDS | REVIEW | DRIFTED |
|---|---|---|---|
| framing r | ≥ 0.55 | 0.30 to 0.55 | < 0.30 |
| palette distance (0..1, 4x4 mean RGB) | ≤ 0.25 | > 0.25 with framing ≥ 0.55 | > 0.25 with framing < 0.55 |
| duration | ≥ shot length | | shorter |
| aspect | within 2% | | otherwise |

Confidence: the thresholds are calibrated on synthetic plates only (an
identical picture scores r = 1.0, palette 0.00; an unrelated one r ≈ 0.2,
palette ≈ 0.43). They will move after the first real credit test. Treat
REVIEW as "look at it", not as a pass.

Frames are scaled after conversion to the target pixel format. Scaling a
4:2:0 YUV frame before converting to RGB gave a palette distance of 0.15 for an
identical picture during the build; converting first gives 0.001.

## Sources

1. Higgsfield MCP tool schemas (`estimate_video_cost`, `generate_video`, `jobs_wait`, `media_upload`, `models_explore`), read live 2026-11-26. Primary source for every Higgsfield rule above.
2. Model Context Protocol specification, Tools: https://modelcontextprotocol.io/specification — tools are discovered at run time with `tools/list`, which is why adapters name roles, not fixed call sites.
3. Z. Wang, A. C. Bovik, H. R. Sheikh, E. P. Simoncelli, "Image quality assessment: from error visibility to structural similarity", IEEE Transactions on Image Processing 13(4), 2004, pp. 600-612.
4. FFmpeg filters documentation (`scale`, `format`, `-sseof`): https://ffmpeg.org/ffmpeg-filters.html
5. Regulation (EU) 2024/1689 (AI Act), Article 50, transparency obligations for deployers of systems that generate or manipulate video. Check the text that applies to your publication; this plugin only reminds you to label.
6. This plugin's `video-director/references/previz_pipeline.md` for why spend follows an approved animatic.
