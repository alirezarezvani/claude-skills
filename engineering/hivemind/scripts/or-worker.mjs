#!/usr/bin/env node
// or-worker.mjs — a hivemind worker backed by OpenRouter instead of opencode.
//
// Same one-JSON-line contract as oc-worker.mjs, so oc-verify.mjs, oc-status.mjs
// and every caller work unchanged. Use this when opencode's free tier is down
// (it 404s and returns empty responses often enough to matter) or when the
// worker has to run somewhere without opencode installed, such as CI.
//
//   node or-worker.mjs --model <id> [--dir <path>] [--files "a.md,b.txt"]
//                      [--system <text>] [--json] [--run id --label name]
//                      [--timeout 900] "TASK TEXT"
//
// Key: read from OPENROUTER_API_KEY, else ~/.claude/.openrouter_key.
// The key is never logged, never echoed, and never included in output.

import { readFileSync, readdirSync, statSync, mkdirSync, appendFileSync } from "node:fs";
import { join, dirname, relative } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";

const API = "https://openrouter.ai/api/v1/chat/completions";
const DEFAULT_MODEL = "google/gemini-2.5-flash";
const RUNS_DIR = join(dirname(dirname(fileURLToPath(import.meta.url))), ".runs");
const MAX_FILE_BYTES = 60_000;

let RUN = null, LABEL = null;

function emit(o) { console.log(JSON.stringify(o)); process.exit(0); }
function fail(stage, error, extra = {}) {
  logRun("fail", { stage, error: String(error).slice(0, 300) });
  emit({ ok: false, stage, error: String(error).slice(0, 300), result: "", tokens: null, cost_usd: null, duration_ms: 0, ...extra });
}
function logRun(event, extra = {}) {
  if (!RUN) return;
  try {
    mkdirSync(RUNS_DIR, { recursive: true });
    appendFileSync(join(RUNS_DIR, `${RUN}.jsonl`), JSON.stringify({ ts: Date.now(), event, label: LABEL, ...extra }) + "\n");
  } catch {}
}

function apiKey() {
  const env = process.env.OPENROUTER_API_KEY;
  if (env && env.trim()) return env.trim();
  try {
    const k = readFileSync(join(homedir(), ".claude", ".openrouter_key"), "utf8").trim();
    if (k) return k;
  } catch {}
  return null;
}

function parseArgs(argv) {
  const o = { model: DEFAULT_MODEL, dir: null, files: null, system: null, json: false,
              run: null, label: null, timeoutMs: 900_000, maxTokens: 8000, task: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--model") o.model = argv[++i] ?? o.model;
    else if (a === "--dir") o.dir = argv[++i] ?? null;
    else if (a === "--files") o.files = (argv[++i] || "").split(",").map(s => s.trim()).filter(Boolean);
    else if (a === "--system") o.system = argv[++i] ?? null;
    else if (a === "--json") o.json = true;
    else if (a === "--run") o.run = argv[++i] ?? null;
    else if (a === "--label") o.label = argv[++i] ?? null;
    else if (a === "--timeout") o.timeoutMs = (Number(argv[++i]) || 900) * 1000;
    else if (a === "--max-tokens") o.maxTokens = Number(argv[++i]) || o.maxTokens;
    else o.task.push(a);
  }
  o.task = o.task.join(" ").trim();
  return o;
}

// The worker has no filesystem tools, so the caller's directory is inlined into
// the prompt. Bounded per file and in total, because an unbounded read is how a
// "cheap" worker turns into an expensive one.
function collect(dir, only) {
  const out = [];
  let budget = 400_000;
  const walk = (d) => {
    let entries;
    try { entries = readdirSync(d); } catch { return; }
    for (const name of entries.sort()) {
      if (budget <= 0) return;
      const full = join(d, name);
      let st;
      try { st = statSync(full); } catch { continue; }
      if (st.isDirectory()) { if (name !== ".git" && name !== "node_modules") walk(full); continue; }
      const rel = relative(dir, full).split("\\").join("/");
      if (only && !only.includes(rel)) continue;
      if (st.size > MAX_FILE_BYTES) { out.push(`--- ${rel} (${st.size} bytes, skipped: too large)`); continue; }
      let body;
      try { body = readFileSync(full, "utf8"); } catch { continue; }
      if (/\u0000/.test(body)) { out.push(`--- ${rel} (binary, skipped)`); continue; }
      const chunk = `--- ${rel}\n${body}`;
      budget -= chunk.length;
      out.push(chunk);
    }
  };
  walk(dir);
  return out.join("\n\n");
}

function extractJson(text) {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  for (const c of [fenced ? fenced[1] : null, text].filter(Boolean)) {
    const s = c.trim();
    for (const [open, close] of [["[", "]"], ["{", "}"]]) {
      const i = s.indexOf(open), j = s.lastIndexOf(close);
      if (i !== -1 && j > i) { try { return JSON.parse(s.slice(i, j + 1)); } catch {} }
    }
    try { return JSON.parse(s); } catch {}
  }
  return null;
}

async function callModel(key, opts, messages) {
  const res = await fetch(API, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${key}`,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://github.com/Hanishchow/hivemind",
      "X-Title": "hivemind",
    },
    body: JSON.stringify({
      model: opts.model,
      messages,
      // Without an explicit ceiling OpenRouter reserves the model's maximum and
      // rejects the call with 402 on a small balance, even for a tiny reply.
      max_tokens: opts.maxTokens,
      ...(opts.json ? { response_format: { type: "json_object" } } : {}),
    }),
    signal: AbortSignal.timeout(opts.timeoutMs),
  });
  const text = await res.text();
  if (!res.ok) {
    // Never surface the body verbatim past a bound; it can echo request detail.
    const stage = res.status === 402 ? "credit" : res.status === 429 ? "ratelimit" : "api";
    return { ok: false, stage, error: `HTTP ${res.status}: ${text.slice(0, 200)}` };
  }
  let body;
  try { body = JSON.parse(text); } catch { return { ok: false, stage: "parse", error: "response was not JSON" }; }
  const content = body?.choices?.[0]?.message?.content;
  if (!content) return { ok: false, stage: "empty", error: "model returned no content" };
  const u = body.usage || {};
  return {
    ok: true,
    content,
    tokens: { total: u.total_tokens ?? null, input: u.prompt_tokens ?? null, output: u.completion_tokens ?? null },
    cost_usd: typeof u.cost === "number" ? u.cost : null,
  };
}

async function main() {
  const t0 = Date.now();
  const opts = parseArgs(process.argv.slice(2));
  RUN = opts.run; LABEL = opts.label || "or-worker";
  if (!opts.task) fail("args", "no task given");

  const key = apiKey();
  if (!key) fail("args", "no API key: set OPENROUTER_API_KEY or ~/.claude/.openrouter_key");

  let context = "";
  if (opts.dir) {
    try { if (!statSync(opts.dir).isDirectory()) fail("args", `--dir is not a directory: ${opts.dir}`); }
    catch { fail("args", `--dir does not exist: ${opts.dir}`); }
    context = collect(opts.dir, opts.files);
    if (!context) fail("args", `--dir contained no readable files: ${opts.dir}`);
  }

  logRun("start", { model: opts.model, dir: opts.dir });

  const system = opts.system ||
    "You are a precise analysis worker. Judge only from the material you are given. " +
    "Never invent files, features, numbers, or commands you cannot see. " +
    "If something cannot be determined from the material, say so plainly instead of guessing." +
    (opts.json ? " Reply with the JSON value only: no prose, no markdown fence." : "");

  const user = context ? `${opts.task}\n\nFILES:\n\n${context}` : opts.task;
  const messages = [{ role: "system", content: system }, { role: "user", content: user }];

  let r = await callModel(key, opts, messages);
  if (!r.ok) fail(r.stage, r.error, { duration_ms: Date.now() - t0, model: opts.model });

  let payload = r.content;
  if (opts.json) {
    let value = extractJson(r.content);
    if (value === null) {
      const retry = await callModel(key, opts, [...messages,
        { role: "assistant", content: r.content },
        { role: "user", content: "That could not be parsed. Reply with the JSON value ONLY - no prose, no fence." }]);
      if (retry.ok) {
        value = extractJson(retry.content);
        for (const k of ["total", "input", "output"]) {
          if (r.tokens[k] != null && retry.tokens?.[k] != null) r.tokens[k] += retry.tokens[k];
        }
      }
    }
    if (value === null) fail("schema", "worker did not return parseable JSON after a corrective retry",
      { duration_ms: Date.now() - t0, model: opts.model });
    payload = JSON.stringify(value);
  }

  const duration = Date.now() - t0;
  logRun("done", { tokens_total: r.tokens?.total ?? null, duration_ms: duration });
  emit({
    ok: true,
    json: opts.json || undefined,
    result: payload.slice(-20000),
    tokens: r.tokens,
    cost_usd: r.cost_usd,
    duration_ms: duration,
    label: LABEL,
    provider: "openrouter",
    model: opts.model,
  });
}

main().catch(e => fail("crash", e?.stack || e));
