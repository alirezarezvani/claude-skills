#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# validate_examples.py — the drift gate for DESIGN.md, memory_schema.json, and
# the worked examples they share.
#
# WHY IT EXISTS: across this design's review, drift between DESIGN.md, the
# schema, and the fixtures was the DOMINANT defect class — required-field
# drift, a tier the examples never exercised, hashes that stopped reproducing,
# headings inserted out of order, a confidence value that contradicted its own
# lifecycle narrative. Every one was found by a check like the ones below.
# Those checks had lived only in throwaway shell heredocs, so they died with
# the session that wrote them. This file is where they live now.
#
# WHAT IT GUARDS, in seven families: schema conformance · the tier-dependent
# back-pointer form · reproduction of the ids DESIGN.md publishes, from the
# doc's own normalize() algorithm · confidence monotonicity and gate
# compliance · document structure and links · prose claims that must match
# measured reality · lifecycle coherence across a multi-tier id group.
#
# It compares the doc's published algorithm to this file's implementation by
# SOURCE TEXT, deliberately not by exec()-ing the doc's fenced block. That
# earlier approach made "whoever can edit a code fence" equal to "whoever can
# run arbitrary code" — a real vector the moment this file is wired into
# pull_request-triggered CI.
#
# NOT WIRED INTO CI. Nothing runs it automatically; DESIGN.md 10.1 carries the
# exact workflow step for whoever wants it. Run it by hand before any edit to
# this folder lands.
#
# stdlib only. No jsonschema (not available repo-wide) — this is a partial
# validator covering exactly this design's own failure modes, not a general
# JSON Schema implementation. That narrowness is deliberate: a general
# validator would be a dependency, and the allOf branches here are the only
# ones that have ever actually drifted.
# ---------------------------------------------------------------------------
import hashlib
import inspect
import json
import os
import re
import sys

def _find(start, marker, limit=10):
    """Walk up from `start` until `marker` is satisfied. `marker` is either a
    filename or a predicate taking a directory path.

    NOT `dirname(dirname(__file__))`. That form is correct only at this file's
    CURRENT depth (assets/, two below the plugin root). §10.1 moves this script
    to skills/agent-memory/scripts/ — four below — where a fixed dirname-count
    silently lands on the SKILL root instead: SCHEMA would still resolve (by
    coincidence, since assets/ and scripts/ become siblings) while DESIGN would
    not, so every check that reads the doc would stop running.

    Anchoring on a marker file makes the script correct at any depth, so the
    move in §10.1 cannot quietly disable a check.
    """
    hit = marker if callable(marker) else (
        lambda d: os.path.exists(os.path.join(d, marker)))
    d = os.path.abspath(start)
    for _ in range(limit):
        if hit(d):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise SystemExit(
        "FATAL: could not locate %s by walking up from %s.\n"
        "  This checker anchors its paths on that marker rather than a fixed\n"
        "  directory depth. If the layout changed, update the marker — do not\n"
        "  fall back to a dirname count, which fails silently on a move."
        % (marker, start)
    )


BASE = _find(os.path.dirname(os.path.abspath(__file__)), "DESIGN.md")
DESIGN = os.path.join(BASE, "DESIGN.md")
SCHEMA = os.path.join(BASE, "assets", "memory_schema.json")
if not os.path.exists(SCHEMA):  # post-§10.1 layout: assets/ moves under the skill
    SCHEMA = os.path.join(BASE, "skills", "agent-memory", "assets",
                          "memory_schema.json")

CONFIDENCE_ORDER = ["observed", "stated", "verified"]
GATE_SESSIONS = {"observed": 3, "stated": 2, "verified": 1}

failures = []
ran = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    ran.append(label)
    if not cond:
        failures.append(label)


def norm_prose(text):
    """Case, whitespace and markdown markers all normalized ONCE.

    Repeated false FAILs came from assertions matching a
    literal string that had wrapped, changed case, or sat inside backticks.
    Normalizing here is the fix for all three at once.
    """
    return re.sub(r"\s+", " ", re.sub(r"[`*_>]", "", text)).casefold()


def load():
    schema = json.load(open(SCHEMA))
    design = open(DESIGN).read()
    return schema, design


def atom_examples(schema, design):
    """Every atom in the repo: the schema's own examples PLUS every JSON block
    in DESIGN.md. A `tier` drift once survived because only the former was
    checked."""
    out = [("schema[%d]" % i, e) for i, e in enumerate(schema["examples"], 1)]
    for j, block in enumerate(re.findall(r"```json\n(.*?)\n```", design, re.S), 1):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "id" in obj:
            out.append(("DESIGN[%d]" % j, obj))
    return out


def normalize(claim):
    """The algorithm DESIGN.md §4.1 publishes. Kept in sync by the check below,
    NOT by executing the doc."""
    return re.sub(r"\s+", " ", claim.strip()).casefold().rstrip(".,;:!?")


def published_normalize(design):
    """Assert the §4.1 fence matches the normalize() above, then return ours.

    The property worth having is that the doc's algorithm and the fixtures'
    ids cannot silently diverge -- two ids once shipped that did not reproduce,
    because nothing tied the prose to the fixtures.

    This file got that property by `exec`-ing the fenced block until it was
    caught in review. That worked, but made "whoever can edit a code fence"
    equal to
    "whoever can run arbitrary code in this process" -- the exact eval-family
    shape this repo ships engineering/security-guidance to flag. Harmless while
    a maintainer runs this by hand on a branch they already trust; NOT harmless
    the moment it is wired into CI, which .github/workflows/ci-quality-gate.yml
    triggers on `pull_request`. That would have handed code execution to any PR
    author, including from a fork, via a prose file nobody reads as executable.
    The safety of the exec depended on a fact outside this file, and the
    obvious next step (gate it in CI) silently falsified that fact.

    Comparing source text instead keeps the anti-divergence property with no
    execution at all: edit the doc's block and this fails until the copy above
    is updated to match. It fails closed on a cosmetic reformat too -- an
    acceptable trade, since the failure says "sync these two" rather than
    running whatever the fence now contains.
    """
    match = re.search(r"def normalize.*?\n```", design, re.S)
    if match is None:
        raise SystemExit(
            "FATAL: could not find the normalize() definition fenced in "
            "DESIGN.md §4.1.\n"
            "  This checker verifies its own copy of the algorithm against the "
            "doc's published one, so if that fence moves or is renamed, id "
            "verification cannot run and must not be silently skipped.\n"
            "  Fix: restore a ```python fence defining normalize() in §4.1, or "
            "update this extractor to match its new location."
        )
    published = match.group(0).rsplit("```", 1)[0]
    mine = inspect.getsource(normalize)
    # Compare the one line that carries the behaviour. Docstrings, type hints
    # and blank lines differ between the two copies by design.
    def _body(src):
        return re.sub(r"\s+", " ", "".join(
            ln.strip() for ln in src.splitlines() if ln.strip().startswith("return")))
    if _body(published) != _body(mine):
        raise SystemExit(
            "FATAL: DESIGN.md §4.1's normalize() no longer matches this "
            "checker's copy.\n"
            "  published: %s\n  checker:   %s\n"
            "  The doc is the contract. Update normalize() in this file to "
            "match, in the same commit that changed the doc -- ids verified "
            "against a stale algorithm prove nothing."
            % (_body(published), _body(mine))
        )
    return normalize


def atom_id(normalize, claim, project=None):
    key = normalize(claim) + ("\0" + project if project else "")
    return "atm_" + hashlib.sha256(key.encode()).hexdigest()[:8]


def main():
    schema, design = load()
    flat = norm_prose(design)
    required = set(schema["required"])
    # Do NOT whitelist `$comment` here (this line once did, weakening the
    # checker to excuse an annotation embedded in an example). `examples` are
    # INSTANCE data, so additionalProperties:false forbids it; $comment is a
    # schema keyword, legal only at schema level and in the allOf branches.
    props = set(schema["properties"])
    examples = atom_examples(schema, design)
    normalize = published_normalize(design)

    # -- family 1: every atom satisfies the schema it claims to demonstrate ---
    for name, ex in examples:
        check(not (required - set(ex)), "%s has all required fields" % name)
        check(not (set(ex) - props), "%s declares no unknown fields" % name)
        check(("project" in ex) == (ex["scope"] == "project"),
              "%s scope<->project conditional" % name)
        want_scope = "project" if ex["tier"] in ("L1", "L2") else "global"
        check(ex["scope"] == want_scope, "%s tier->scope conditional" % name)
        if ex["tier"] == "L3":
            check(len(set(ex.get("promoted_from_projects", []))) >= 2,
                  "%s L3 carries >=2 promoted_from_projects" % name)
        if ex["tier"] in ("L2", "L3"):
            # §4.1.1's 30-day age gate and §4.3's demotion both key off this;
            # an atom that reached a committed tier without it could never
            # satisfy the age test and would sit un-promotable, silently.
            check("promoted_at" in ex,
                  "%s committed tier records promoted_at" % name)
        check(len(ex["sessions"]) == len(set(ex["sessions"])),
              "%s sessions unique" % name)

    # -- family 2: the tier-dependent back-pointer (the PII-consequence rule) --
    L1_PAT = r"^~/\.claude/projects/[^/]+/[A-Za-z0-9._-]+\.jsonl#L[0-9]+$"
    CM_PAT = r"^[A-Za-z0-9._-]+\.jsonl#L[0-9]+$"
    for name, ex in examples:
        pat = L1_PAT if ex["tier"] == "L1" else CM_PAT
        for field in ("source", "first_source"):
            check(re.match(pat, ex[field]) is not None,
                  "%s %s matches its tier's back-pointer form" % (name, field))
    # the rule must REJECT the leak it exists to prevent, not merely accept
    # the fixtures -- asserting only the happy path misses exactly this class.
    check(re.match(CM_PAT, "~/.claude/projects/-home-alice/X.jsonl#L1") is None,
          "REJECTS an unstripped L2/L3 back-pointer (the OS-username leak)")
    check(re.match(L1_PAT, "X.jsonl#L1") is None,
          "REJECTS a prefix-less L1 back-pointer")

    # -- family 3: ids reproduce from the doc's OWN published algorithm -------
    for name, ex in examples:
        check(atom_id(normalize, ex["claim"], ex.get("project")) == ex["id"],
              "%s id reproduces from the published normalize()+sha256" % name)
    # L1->L2 keeps the id; L2->L3 mints a new one (project component drops)
    l2 = [e for _, e in examples if e["tier"] == "L2"]
    if l2:
        c, p = l2[0]["claim"], l2[0]["project"]
        check(atom_id(normalize, c, p) != atom_id(normalize, c),
              "L2->L3 mints a NEW project-free id, as §4.1.1 states")

    # -- family 4: confidence is a legal, monotonic lifecycle ----------------
    by_id = {}
    for name, ex in examples:
        by_id.setdefault(ex["id"], []).append(ex)
    for aid, group in by_id.items():
        for ex in group:
            check(ex["confidence"] in CONFIDENCE_ORDER,
                  "%s confidence is a declared value" % aid)
            # The session-count gate is the L1 -> L2 rule and ONLY that.
            # L1 is pre-gate by definition. L3 is gated on >= 2 distinct
            # projects plus age (4.1.1), not on sessions at all -- so an
            # `or tier == "L1"` exemption alone left this check firing on L3
            # against a rule that does not govern it, where it passed for an
            # incidental reason (L3 inherits the unioned sessions of L2
            # contributors that each already cleared their own gate). A check
            # that cannot fail on a tier is not testing that tier.
            if ex["tier"] == "L2":
                check(len(ex["sessions"]) >= GATE_SESSIONS[ex["confidence"]],
                      "%s clears the session gate its confidence implies" % aid)
            # 4.1's gate is TWO clauses -- session count AND >= 2 distinct
            # calendar days (UTC) -- and only the count half was checked. The
            # days clause is the half that stops one long working day from
            # minting an L2 claim, which is exactly the case 4.1 calls out for
            # the `stated` fast path. `verified` is the one exempt path.
            #
            # first_seen/last_seen BOUND every observation, so
            # date(first) != date(last) is not an approximation of ">= 2
            # distinct days" -- it is equivalent to it. Same date means every
            # observation fell inside that date; different dates means at
            # least two were touched.
            if ex["tier"] == "L2" and ex["confidence"] != "verified":
                check(ex["first_seen"][:10] != ex["last_seen"][:10],
                      "%s spans >= 2 distinct calendar days, the half of the "
                      "4.1 gate session-count does not cover" % aid)
            if ex["tier"] == "L3":
                check(len(set(ex.get("promoted_from_projects", []))) >= 2,
                      "%s clears the >= 2-distinct-projects gate L3 actually has"
                      % aid)
        if len(group) > 1:
            ordered = sorted(group, key=lambda e: ["L1", "L2", "L3"].index(e["tier"]))
            for a, b in zip(ordered, ordered[1:]):
                check(CONFIDENCE_ORDER.index(b["confidence"])
                      >= CONFIDENCE_ORDER.index(a["confidence"]),
                      "%s confidence never downgrades across tiers" % aid)

    # -- family 5: document structure (headings, links, fixtures) ------------
    heads = [(len(h), tuple(int(x) for x in n.split(".")))
             for h, n, _ in re.findall(r"^(#{2,6}) (\d+(?:\.\d+)*)\.?\s+(.*)$",
                                       design, re.M)]
    check(all(lvl == len(num) + 1 for lvl, num in heads),
          "heading level equals numbering depth everywhere")
    nums = [n for _, n in heads]
    check(all(nums[i] > nums[i - 1] for i in range(1, len(nums))),
          "heading numbers ascend in document order")
    # links inside code spans are literal text, not links
    for target in set(re.findall(r"\]\((?!http)([^)#]+)\)",
                                 re.sub(r"`[^`\n]*`", "", design))):
        check(os.path.exists(os.path.join(BASE, target)),
              "relative link resolves: %s" % target)
    # fixtures obey the admission policy the doc itself specifies (§6.5)
    blob = json.dumps([e for _, e in examples]) + design
    # Both places a project name can appear, not just one. Checking only the
    # path-embedded form (`-home-user-<slug>`) left `project` and
    # `promoted_from_projects` -- where names appear bare -- entirely
    # unchecked, so "other-project" in the allow-list was inert and a fixture
    # naming a private repo in those fields would have passed. 6.5's rule is
    # about the name, not about where it happens to sit.
    known = {"claude-skills", "other-project"}
    named = set(re.findall(r"-home-user-([a-z0-9._-]+)", blob))
    for _, e in examples:
        if "project" in e:
            named.add(e["project"])
        named.update(e.get("promoted_from_projects", []))
    check(not (named - known),
          "no unknown project names in fixtures, in paths or in fields %s"
          % sorted(named - known))
    ids = {s for _, e in examples for s in e["sessions"]}
    check(all(i.startswith("01SESSION") for i in ids),
          "all fixture session ids are synthetic")

    # -- family 6: claims in prose that must match measurable reality --------
    # The 1 size claim is a POINT-IN-TIME measurement, so this family checks
    # what the doc controls, not what it does not. Do NOT compare the cited
    # figure against the live byte count of repo-root CLAUDE.md: that file gets
    # a release note on nearly every point release, so the check would go red on
    # unrelated PRs. Snapshotting it as a constant here is no better -- the same
    # number in a second place, with nothing able to say which drifted. What is
    # durable, and what the original defect was ("~40 KB", eyeballed, off by
    # >2x): the claim must name its method, carry a real byte figure, and have
    # its two units agree. All properties of the sentence itself.
    m = re.search(r"\*\*(\d+) KB\*\*[^.]*?`wc -c`[^.]*?([\d,]{4,})\s+bytes", design)
    check(m is not None,
          "the CLAUDE.md size claim names `wc -c` and cites a byte figure")
    if m:
        kb, byts = int(m.group(1)), int(m.group(2).replace(",", ""))
        check(round(byts / 1024) == kb,
              "the size claim's KB and byte figures agree (%d KB == %d bytes)"
              % (kb, byts))
    check("not observations" in flat,
          "promotion row names sessions, not observations, as the gate")

    # 4.1.1's merge step must account for EVERY schema-required field, not the
    # interesting ones -- repeated omissions there (`source`,
    # `promoted_from_projects`, confidence/redacted/kind) were each caught by a
    # human reading the list against the schema. This is the class, not another
    # instance: an implementation written literally against a step that skips a
    # required field emits a schema-invalid atom.
    merge = design[design.index("#### 4.1.1"):design.index("#### 4.1.2")]
    merge_flat = norm_prose(merge)
    # norm_prose strips `_` (a markdown italic marker), so field names must be
    # normalized the SAME way before matching -- searching for "first_seen" in
    # text where it has become "firstseen" reports a false gap.
    missing = [f for f in schema["required"] if norm_prose(f) not in merge_flat]
    # Limit, stated rather than implied: this is a substring test over the whole
    # section, so a field named incidentally elsewhere in 4.1.1 (`confidence`
    # and `claim` both appear in the fast-paths and the lexical-limit
    # paragraphs) satisfies it without the merge step actually specifying it.
    # Re-injecting the real omission proves it still catches `kind` and
    # `redacted`, which had no other mention. A tighter check would have to
    # parse the merge step itself and would break on any rewording. Like
    # 4.2.1's detector, this is a filter, not a guarantee.
    check(not missing,
          "4.1.1's merge accounts for every schema-required field %s" % missing)

    # -- family 7: the lifecycle pair actually coheres in time ---------------
    # Added after a review found the L1 fixture in DESIGN.md 3.1 and the L2
    # example in the schema -- explicitly captioned "one atom's lifecycle,
    # read side by side" -- contradicting each other: the L1 snapshot carried
    # the L2's *last_seen* as its own first_seen (making the first sighting
    # postdate the promotion by three weeks) and the L2's *source* line number
    # where its first_source belonged. Families 1-6 all passed on it, because
    # each atom was independently well-formed; nothing compared them. That is
    # the point of this family: a prose claim that two fixtures are one story
    # imposes constraints no per-atom check can see.
    for aid, group in by_id.items():
        for ex in group:
            check(ex["first_seen"] <= ex["last_seen"],
                  "%s/%s first_seen precedes last_seen" % (aid, ex["tier"]))
            if "promoted_at" in ex:
                check(ex["first_seen"] <= ex["promoted_at"] <= ex["last_seen"],
                      "%s/%s promoted_at falls inside its own observation window"
                      % (aid, ex["tier"]))
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda e: ["L1", "L2", "L3"].index(e["tier"]))
        for a, b in zip(ordered, ordered[1:]):
            # 4.1.1 step 3: promotion takes min(first_seen), so the earliest
            # timestamp survives promotion unchanged -- it can never move.
            check(a["first_seen"] == b["first_seen"],
                  "%s first_seen is identical across tiers (promotion takes min)"
                  % aid)
            check(a["last_seen"] <= b["last_seen"],
                  "%s last_seen never moves backwards up a tier" % aid)
            check(a["observations"] <= b["observations"],
                  "%s observations accumulate up a tier" % aid)
            check(set(a["sessions"]) <= set(b["sessions"]),
                  "%s sessions are a superset up a tier (promotion unions them)"
                  % aid)
            # 3.1.1 strips the path prefix and NOTHING else, so the lower
            # tier's own back-pointer must survive as the upper tier's
            # first_source with only the prefix removed. A differing line
            # number means one of the two was invented.
            check(a["first_source"].split("/")[-1] == b["first_source"],
                  "%s first_source survives promotion with only the path "
                  "prefix stripped" % aid)

    # The doc states how many checks this file runs. That sentence went stale
    # twice while the section containing it argued against exactly this kind of
    # drift, and a reviewer then quoted the stale number back. So the program
    # owns the claim: `+ 1` accounts for this check itself, which has not been
    # appended to `ran` yet at the moment the count is computed. Keep this LAST
    # -- any check added after it silently invalidates the arithmetic.
    _total = len(ran) + 1
    check("%d checks in seven families" % _total in norm_prose(design),
          "DESIGN.md cites the number of checks this file actually runs")

    print("\n%d checks, %d failures" % (len(ran), len(failures)))
    for f in failures:
        print("  FAILED: " + f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
