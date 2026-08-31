#!/usr/bin/env node
// oc-verify.mjs — runs a verifier worker over another worker's claims so the
// orchestrator does not have to re-check every one by hand.
//
//   node oc-verify.mjs --dir <path> --claims <file.json|-> [--run id] [--label name]
//                      [--model <p/m>] [--timeout 900]
//
// --claims takes the JSON array a scout produced (or "-" to read stdin). Each
// element is stringified into a numbered claim list for the verifier.
//
// Prints ONE JSON line:
//   { ok, confirmed, refuted, unsupported, needs_review:[...], verdicts:[...],
//     tokens, cost_usd, duration_ms }
//
// needs_review holds only the REFUTED and UNSUPPORTED items — that is the
// short list a human or an expensive model should actually look at. Confirmed
// claims are reported as counts, not re-litigated.

import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
// A verifier on the same model as the worker shares its blind spots, so the
// default is deliberately a different free model.
const DEFAULT_VERIFIER_MODEL = "opencode/nemotron-3.5-lightning-free";

function out(o) { console.log(JSON.stringify(o)); process.exit(0); }

function parseArgs(argv) {
  const o = { dir: null, claims: null, run: null, label: "verify", model: null, timeout: "900" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--dir") o.dir = argv[++i];
    else if (a === "--claims") o.claims = argv[++i];
    else if (a === "--run") o.run = argv[++i];
    else if (a === "--label") o.label = argv[++i];
    else if (a === "--model") o.model = argv[++i];
    else if (a === "--timeout") o.timeout = argv[++i];
  }
  return o;
}

const opts = parseArgs(process.argv.slice(2));
if (!opts.claims) out({ ok: false, stage: "args", error: "--claims is required" });

let claims;
try {
  const raw = opts.claims === "-" ? readFileSync(0, "utf8") : readFileSync(opts.claims, "utf8");
  claims = JSON.parse(raw);
  if (!Array.isArray(claims)) claims = [claims];
} catch (e) {
  out({ ok: false, stage: "args", error: `could not read claims: ${String(e).slice(0, 120)}` });
}
if (claims.length === 0) out({ ok: true, confirmed: 0, refuted: 0, unsupported: 0, needs_review: [], verdicts: [] });

const numbered = claims
  .map((c, i) => `${i + 1}. ${typeof c === "string" ? c : JSON.stringify(c)}`)
  .join("\n");

const task =
  `Another worker inspected the files in this directory and produced the claims below. ` +
  `Verify each one against the files. Try to refute them.\n\n${numbered}\n\n` +
  `Return a JSON array with one object per numbered claim, in the same order.`;

const args = [
  join(HERE, "oc-worker.mjs"),
  "--agent", "verifier",
  "--model", opts.model || DEFAULT_VERIFIER_MODEL,
  "--timeout", opts.timeout,
  "--json",
];
if (opts.dir) args.push("--dir", opts.dir);
if (opts.run) args.push("--run", opts.run, "--label", opts.label);
args.push(task);

const r = spawnSync("node", args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
const line = (r.stdout || "").trim().split("\n").filter(Boolean).pop();
if (!line) out({ ok: false, stage: "exec", error: "verifier produced no output" });

let w;
try { w = JSON.parse(line); } catch { out({ ok: false, stage: "parse", error: "verifier output was not JSON" }); }
if (!w.ok) out({ ok: false, stage: w.stage || "worker", error: w.error || "verifier failed" });

let verdicts;
try { verdicts = JSON.parse(w.result); } catch { out({ ok: false, stage: "schema", error: "verifier result was not a JSON array" }); }
if (!Array.isArray(verdicts)) verdicts = [verdicts];

const norm = (v) => String(v || "").toUpperCase();
const confirmed = verdicts.filter((v) => norm(v.verdict) === "CONFIRMED");
const refuted = verdicts.filter((v) => norm(v.verdict) === "REFUTED");
const unsupported = verdicts.filter((v) => norm(v.verdict) === "UNSUPPORTED");

// A verifier that returns fewer verdicts than there were claims has skipped
// some; silently dropping them would let unchecked claims pass as verified.
const missing = claims.length - verdicts.length;

out({
  ok: true,
  claims: claims.length,
  confirmed: confirmed.length,
  refuted: refuted.length,
  unsupported: unsupported.length,
  unverified: missing > 0 ? missing : 0,
  needs_review: [...refuted, ...unsupported],
  verdicts,
  tokens: w.tokens,
  cost_usd: w.cost_usd,
  duration_ms: w.duration_ms,
  verifier_model: opts.model || DEFAULT_VERIFIER_MODEL,
});
