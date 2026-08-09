#!/usr/bin/env python3
"""The human-verification gate for an agent loop.

Machine verification answers "do the checks pass?". This answers the other
question — "has a person actually looked at it, and are their objections
resolved?" — and refuses to let the loop close until they are.

Subcommands
-----------
    open <artifact>      build the review page, start (or advance) a round
    status <artifact>    is feedback waiting? non-blocking, exit-code driven
    collect <artifact>   parse the sidecar, record the round, emit batch.v1
    close <artifact>     the gate: refuses while review is missing or open
    reset <artifact>     discard gate state for this artifact

Gate rules
----------
    G1  close refuses if no review round was ever collected
    G2  close refuses while any BLOCKER or MAJOR item is open
    G3  close refuses without a named reviewer (approval belongs to a person)
    G4  close refuses if the sidecar changed after the last collect
    G5  rounds are capped (--max-rounds); exhaustion escalates, it never
        silently keeps looping
    G6  a waiver is allowed but must be explicit, reasoned, and recorded --
        and it can never waive G1: no waiver substitutes for review happening
    G7  close refuses while the last round carries unresolved integrity
        problems (mistyped severity, EDIT with no replacement, a quote not
        in the file) — those downgrade silently, so prose is not enough

Loop discipline
---------------
There is no blocking poll here, by design. `status` returns immediately and
the agent ends its turn. On a headless host `open` says so plainly instead of
telling the agent to wait at a browser that will never appear.

Exit codes
----------
    0  ok / gate passed
    1  usage error
    2  gate refuses to close
    3  feedback is waiting to be collected
    4  no feedback yet (status: no sidecar on disk)
    5  round cap exhausted — escalate to a human

`status` returns 2 whenever `close` would refuse — it previews every rule via
the shared gate_refusals(), not just blocking items — so an agent can branch on
the exit code alone: 0 clear, 2 blocked, 3 collect me, 4 nothing yet.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCKING = {"BLOCKER", "MAJOR"}
DEFAULT_MAX_ROUNDS = 5

# Parser problems that already have their own gate rule. Everything else the
# parser reports is an integrity problem the gate must refuse on (G7) — a
# mistyped severity silently downgrades to NIT, so without this a reviewer's
# real blocker can be lost to a typo and close would still pass.
#
# The prefixes are owned by feedback_parser.py, beside the code that emits them,
# and read from the loaded module rather than restated here: matching free text
# across two files is a contract nothing enforces, and a reworded message would
# silently turn a G2/G3 problem into a duplicate ungated G7 refusal. The literal
# below is only a fallback for a parser too old to export the names.
_GATED_ELSEWHERE_FALLBACK = (
    "no 'reviewer:' line",   # G3
    "APPROVE is present alongside",  # G2
)


def _load_parser_module():
    import importlib.util

    path = os.path.join(HERE, "feedback_parser.py")
    spec = importlib.util.spec_from_file_location("hg_feedback_parser", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load feedback_parser.py next to human_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gated_elsewhere_prefixes():
    """Problem prefixes G7 must skip, read from the parser that emits them."""
    try:
        prefixes = tuple(_load_parser_module().GATED_ELSEWHERE)
    except (AttributeError, RuntimeError, OSError, TypeError):
        return _GATED_ELSEWHERE_FALLBACK
    return prefixes or _GATED_ELSEWHERE_FALLBACK


# ------------------------------------------------------------------- state


def state_dir(explicit=None, artifact=None):
    """Where gate state lives: beside the artifact, not beside the caller.

    Keying state by the artifact's realpath but storing it under os.getcwd()
    meant an agent whose shell cwd drifted between turns silently started from
    empty state — `close` would report G1 "nobody has looked at this" for a
    round that really was collected, just from a different directory. It fails
    closed rather than falsely passing, but it loses real feedback, so the
    directory now follows the artifact the same way the sidecar and the review
    page already do. An explicit --state-dir still wins.
    """
    if explicit:
        return os.path.abspath(explicit)
    anchor = os.path.dirname(os.path.realpath(artifact)) if artifact else os.getcwd()
    return os.path.join(anchor, ".human-gate")


def state_path(artifact, explicit=None):
    key = hashlib.sha256(os.path.realpath(artifact).encode("utf-8")).hexdigest()[:16]
    return os.path.join(state_dir(explicit, artifact), "%s.json" % key)


def load_state(artifact, explicit=None):
    path = state_path(artifact, explicit)
    if not os.path.exists(path):
        return {
            "artifact": os.path.realpath(artifact),
            "rounds": [],
            "closed": False,
            "waiver": None,
        }
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def max_rounds_for(state, args):
    """The agreed round cap, from state — not from whatever this call passed.

    A per-invocation flag lets `open` and a later `close` disagree about the
    cap, which makes G5 escalation depend on how the command happened to be
    typed. The cap is agreed once, recorded in state, and reused. Passing
    --max-rounds again is an explicit renegotiation, not a silent override.
    """
    stored = state.get("max_rounds")
    requested = getattr(args, "max_rounds", None)
    if requested is not None:
        if stored is not None and stored != requested:
            print("Round cap changed for this artifact: %d -> %d."
                  % (stored, requested))
        state["max_rounds"] = requested
        return requested
    if isinstance(stored, int) and stored > 0:
        return stored
    return DEFAULT_MAX_ROUNDS


def save_state(state, artifact, explicit=None):
    path = state_path(artifact, explicit)
    directory = os.path.dirname(path)
    os.makedirs(directory, mode=0o700, exist_ok=True)
    try:
        os.chmod(directory, 0o700)
    except OSError:
        pass
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def sidecar_for(artifact, explicit=None):
    if explicit:
        return explicit
    return os.path.splitext(artifact)[0] + ".review.md"


def fingerprint(path):
    """Content hash + mtime, so a re-edited sidecar is never mistaken for stale."""
    try:
        with open(path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()[:16]
        return {"sha": digest, "mtime": os.path.getmtime(path)}
    except OSError:
        return None


# ---------------------------------------------------------------- headless


def headless_reason():
    """Why a browser cannot be shown here, or None when one probably can."""
    for var in ("CI", "GITHUB_ACTIONS", "BUILDKITE", "JENKINS_URL"):
        if os.environ.get(var):
            return "running under %s" % var
    if os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY"):
        return "connected over SSH"
    if sys.platform.startswith("linux") and not (
        os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    ):
        return "no DISPLAY or WAYLAND_DISPLAY"
    return None


# ---------------------------------------------------------------- commands


def cmd_open(args):
    artifact = args.artifact
    if not os.path.exists(artifact):
        sys.stderr.write("Artifact not found: %s\n" % artifact)
        return 1

    state = load_state(artifact, args.state_dir)
    if state["closed"] and not args.reopen:
        print("Gate is already closed for %s. Use --reopen to start a new round."
              % os.path.basename(artifact))
        return 0
    state["closed"] = False

    # `open` pins the cap for the whole loop, so a later status/collect/close
    # inherits it rather than re-deriving one from its own flags.
    cap = max_rounds_for(state, args)
    state["max_rounds"] = cap
    round_number = len(state["rounds"]) + 1
    if round_number > cap:
        print("ESCALATE — %d rounds already spent on %s (cap %d)."
              % (len(state["rounds"]), os.path.basename(artifact), cap))
        print("Stop iterating. Hand this to a human and say what is still contested.")
        return 5

    sidecar = sidecar_for(artifact, args.sidecar)
    page = args.page or (os.path.splitext(artifact)[0] + ".review.html")

    build = subprocess.run(
        [
            sys.executable,
            os.path.join(HERE, "review_page_builder.py"),
            artifact,
            "--output", page,
            "--round", str(round_number),
            "--sidecar", os.path.basename(sidecar),
        ],
        capture_output=True,
        text=True,
    )
    if build.returncode != 0:
        sys.stderr.write(build.stderr or "review_page_builder failed\n")
        return build.returncode

    blocked = headless_reason()
    state["open_round"] = {
        "round": round_number,
        "page": os.path.abspath(page),
        "sidecar": os.path.abspath(sidecar),
        "opened_at": time.time(),
        "headless": blocked,
    }
    save_state(state, artifact, args.state_dir)

    print(build.stdout.strip())
    print("")
    print("Round %d of at most %d." % (round_number, cap))
    if blocked:
        print("Headless host (%s) — not launching a browser." % blocked)
        print("Give the reviewer both paths, then END YOUR TURN. Do not poll.")
        print("  page:    %s" % os.path.abspath(page))
        print("  sidecar: %s  (they can also just write this by hand)" % os.path.abspath(sidecar))
    else:
        print("Open the page, review, then Export feedback to:")
        print("  %s" % os.path.abspath(sidecar))
        if args.launch:
            import webbrowser

            webbrowser.open("file://" + os.path.abspath(page))
            print("Launched in your default browser.")
    print("")
    print("When they are done:  human_gate.py collect %s" % artifact)
    return 0


def cmd_status(args):
    artifact = args.artifact
    state = load_state(artifact, args.state_dir)
    sidecar = sidecar_for(artifact, args.sidecar)
    current = fingerprint(sidecar)
    rounds = state["rounds"]
    cap = max_rounds_for(state, args)

    payload = {
        "artifact": os.path.basename(artifact),
        "rounds_collected": len(rounds),
        "max_rounds": cap,
        "closed": state["closed"],
        "sidecar": sidecar,
        "sidecar_present": current is not None,
    }

    if current is None:
        payload["status"] = "awaiting-review"
        code = 4
    elif rounds and rounds[-1].get("sidecar_sha") == current["sha"]:
        payload["status"] = "collected"
        payload["blocking_open"] = rounds[-1].get("blocking_open", 0)
        # Preview the whole gate, not just blocking items — a round with no
        # named reviewer (G3) or an integrity problem (G7) would still be
        # refused by close, and reporting 0 here would mislead an agent that
        # branches on the exit code.
        payload["would_refuse"] = gate_refusals(state, sidecar)
        code = 0 if not payload["would_refuse"] else 2
    else:
        payload["status"] = "feedback-waiting"
        code = 3

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print("%s — %s" % (payload["artifact"], payload["status"]))
        print("Rounds collected: %d / %d" % (len(rounds), cap))
        if not payload["sidecar_present"]:
            print("No sidecar yet at %s" % sidecar)
        elif payload["status"] == "feedback-waiting":
            print("New feedback ready — run: human_gate.py collect %s" % artifact)
        elif payload.get("would_refuse"):
            print("Collected, but close would refuse:")
            for refusal in payload["would_refuse"]:
                print("  ✗ %s" % refusal)
        else:
            print("Collected and clear — close would pass.")
    return code


def cmd_collect(args):
    artifact = args.artifact
    state = load_state(artifact, args.state_dir)
    sidecar = sidecar_for(artifact, args.sidecar)

    current = fingerprint(sidecar)
    if current is None:
        sys.stderr.write("No sidecar at %s — nothing to collect yet.\n" % sidecar)
        return 4

    cap = max_rounds_for(state, args)
    if len(state["rounds"]) >= cap:
        print("ESCALATE — round cap (%d) reached for %s."
              % (cap, os.path.basename(artifact)))
        print("Stop iterating. Summarise what is still contested and hand it to a human.")
        return 5

    parser_module = _load_parser_module()
    with open(sidecar, "r", encoding="utf-8") as handle:
        text = handle.read()
    batch, problems = parser_module.parse(text, os.path.basename(artifact))
    problems.extend(parser_module.verify_quotes(batch, artifact))

    round_number = len(state["rounds"]) + 1
    batch["round"] = round_number
    state["rounds"].append(
        {
            "round": round_number,
            "collected_at": time.time(),
            "reviewer": batch["reviewer"],
            "sidecar_sha": current["sha"],
            "counts": batch["counts"],
            "blocking_open": batch["blocking_open"],
            "approved": batch["approved"],
            "problems": problems,
        }
    )
    state.pop("open_round", None)
    save_state(state, artifact, args.state_dir)

    if args.output == "json":
        print(json.dumps({"batch": batch, "problems": problems,
                          "round": round_number,
                          "rounds_remaining": cap - round_number}, indent=2))
    else:
        print(parser_module.render_human(batch, problems))
        print("")
        print("Recorded as round %d. %d round(s) left before escalation."
              % (round_number, cap - round_number))
        if batch["items"]:
            print("Apply every item. EDIT items carry `after` across VERBATIM —")
            print("that is the reviewer's own wording, not a suggestion to paraphrase.")
    return 0


def gate_refusals(state, sidecar_path):
    """Every reason `close` would refuse, in rule order.

    Shared with `status` on purpose: the exit-code contract promises status is
    a preview of close, and two hand-maintained copies of this logic would
    drift the first time a rule changed.
    """
    rounds = state["rounds"]
    if not rounds:
        return ["G1 no review round has been collected — nobody has looked at this yet"]

    last = rounds[-1]
    refusals = []
    if last.get("blocking_open"):
        refusals.append(
            "G2 %d BLOCKER/MAJOR item(s) still open from round %d"
            % (last["blocking_open"], last["round"])
        )
    if not last.get("reviewer"):
        refusals.append("G3 round %d has no named reviewer" % last["round"])

    current = fingerprint(sidecar_path)
    if current and current["sha"] != last.get("sidecar_sha"):
        refusals.append(
            "G4 the sidecar changed after round %d was collected — "
            "collect again before closing" % last["round"]
        )

    gated = gated_elsewhere_prefixes()
    for problem in last.get("problems", []):
        if problem.startswith(gated):
            continue
        refusals.append("G7 round %d integrity: %s" % (last["round"], problem))
    return refusals


def cmd_close(args):
    artifact = args.artifact
    state = load_state(artifact, args.state_dir)
    rounds = state["rounds"]
    refusals = gate_refusals(state, sidecar_for(artifact, args.sidecar))

    # A waiver overrides objections a human actually raised. It cannot manufacture
    # a review that never happened — "nobody looked" is not a finding to accept,
    # it is the absence of the thing this gate exists to require. Waiving G1 would
    # make the whole skill opt-out with one flag, which is the most tempting
    # shortcut for an agent under time pressure.
    unwaivable = [r for r in refusals if r.startswith("G1 ")]
    if unwaivable and args.waive:
        print("GATE REFUSED — %s" % os.path.basename(artifact))
        for refusal in unwaivable:
            print("  ✗ %s (NOT WAIVABLE)" % refusal)
        print("")
        print("--waive accepts objections a reviewer raised; it cannot stand in for")
        print("review itself. Open a round and get one collected first.")
        return 2

    if refusals and args.waive:
        state["waiver"] = {
            "reason": args.waive,
            "waived_at": time.time(),
            "refusals": list(refusals),
        }
        refusals = []
    elif not refusals:
        if args.waive:
            print("Note: nothing to waive — the gate passes on its own.")
        # A pass that needed no waiver must not inherit an earlier one, or a
        # genuinely clean round N+1 reports round N's waiver as if it applied.
        state["waiver"] = None

    if refusals:
        print("GATE REFUSED — %s" % os.path.basename(artifact))
        for refusal in refusals:
            print("  ✗ %s" % refusal)
        print("")
        print("Do not report this as done. Either resolve the items above and")
        print("collect another round, or record an explicit --waive \"<reason>\".")
        return 2

    state["closed"] = True
    save_state(state, artifact, args.state_dir)

    print("GATE PASSED — %s" % os.path.basename(artifact))
    if rounds:
        last = rounds[-1]
        print("  reviewer: %s" % (last.get("reviewer") or "(none — waived)"))
        print("  rounds:   %d" % len(rounds))
    if state.get("waiver"):
        print("  WAIVED:   %s" % state["waiver"]["reason"])
        for refusal in state["waiver"]["refusals"]:
            print("            (over: %s)" % refusal)
    return 0


def cmd_reset(args):
    path = state_path(args.artifact, args.state_dir)
    # Only ever remove this skill's own state file. The name is a 16-hex digest
    # of the artifact's realpath, so a hostile artifact name cannot steer the
    # delete anywhere, and a mistyped --state-dir cannot make it hit a real file.
    name = os.path.basename(path)
    if not re.fullmatch(r"[0-9a-f]{16}\.json", name):
        sys.stderr.write("Refusing to delete unexpected state file: %s\n" % path)
        return 1
    if os.path.exists(path):
        os.remove(path)
        print("Gate state cleared for %s" % os.path.basename(args.artifact))
    else:
        print("No gate state to clear for %s" % os.path.basename(args.artifact))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Human-verification gate for an agent loop.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--sample", action="store_true", help="run a scripted end-to-end demo and exit"
    )
    sub = parser.add_subparsers(dest="command")

    def shared(sp):
        sp.add_argument("artifact", help="the file under review")
        sp.add_argument("--sidecar", help="override the sidecar path")
        sp.add_argument("--state-dir", help="override the .human-gate state directory")
        sp.add_argument(
            "--max-rounds", type=int, default=None,
            help="round cap before escalation (default %d). Recorded in gate "
                 "state on the first open and reused by every later command, so "
                 "the cap cannot drift between calls; passing it again changes "
                 "the agreed cap and says so." % DEFAULT_MAX_ROUNDS,
        )
        return sp

    opener = shared(sub.add_parser("open", help="build the review page, start a round"))
    opener.add_argument("--page", help="where to write the review page")
    opener.add_argument("--launch", action="store_true", help="open a browser if possible")
    opener.add_argument("--reopen", action="store_true", help="reopen a closed gate")
    opener.set_defaults(func=cmd_open)

    status = shared(sub.add_parser("status", help="is feedback waiting? (non-blocking)"))
    status.add_argument("--output", choices=["human", "json"], default="human")
    status.set_defaults(func=cmd_status)

    collect = shared(sub.add_parser("collect", help="parse the sidecar, record a round"))
    collect.add_argument("--output", choices=["human", "json"], default="human")
    collect.set_defaults(func=cmd_collect)

    close = shared(sub.add_parser("close", help="the gate — refuses unless satisfied"))
    close.add_argument("--waive", metavar="REASON",
                       help="close over open refusals, recording why")
    close.set_defaults(func=cmd_close)

    reset = shared(sub.add_parser("reset", help="discard gate state"))
    reset.set_defaults(func=cmd_reset)

    args = parser.parse_args(argv)

    if args.sample:
        return run_sample()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


def run_sample():
    """End-to-end demo in a temp dir: open -> status -> collect -> close."""
    import shutil
    import tempfile

    work = tempfile.mkdtemp(prefix="human-gate-sample-")
    try:
        artifact = os.path.join(work, "plan.md")
        with open(artifact, "w", encoding="utf-8") as handle:
            handle.write("# Plan\n\nWe expect a 40% lift in activation.\n\n## Risks\n\nNone identified.\n")
        state = os.path.join(work, ".human-gate")
        base = ["--state-dir", state]

        print("=" * 62)
        print("1. open — build the review page and start round 1")
        print("=" * 62)
        main(["open", artifact] + base)

        print("\n" + "=" * 62)
        print("2. status — before any feedback exists")
        print("=" * 62)
        code = main(["status", artifact] + base)
        print("exit=%d (4 = awaiting review)" % code)

        print("\n" + "=" * 62)
        print("3. close — attempted with no review at all")
        print("=" * 62)
        code = main(["close", artifact] + base)
        print("exit=%d (2 = gate refused)" % code)

        sidecar = os.path.join(work, "plan.review.md")
        with open(sidecar, "w", encoding="utf-8") as handle:
            handle.write(
                "# Review feedback: plan.md\n"
                "<!-- human-gate:v1 target=plan.md round=1 -->\n\n"
                "reviewer: reza\n\n"
                "## BLOCKER b2\n"
                "> We expect a 40% lift in activation.\n"
                "No source for 40%. Cite it or cut it.\n\n"
                "## NOTE\nRisks section is empty — that is itself a risk.\n"
            )

        print("\n" + "=" * 62)
        print("4. collect — a human left one BLOCKER")
        print("=" * 62)
        main(["collect", artifact] + base)

        print("\n" + "=" * 62)
        print("5. close — still refused, the blocker is open")
        print("=" * 62)
        code = main(["close", artifact] + base)
        print("exit=%d (2 = gate refused)" % code)

        with open(sidecar, "w", encoding="utf-8") as handle:
            handle.write(
                "# Review feedback: plan.md\n"
                "<!-- human-gate:v1 target=plan.md round=2 -->\n\n"
                "reviewer: reza\n\n"
                "## APPROVE\nSource added. Good to ship.\n"
            )

        print("\n" + "=" * 62)
        print("6. collect round 2, then close — passes")
        print("=" * 62)
        main(["collect", artifact] + base)
        code = main(["close", artifact] + base)
        print("exit=%d (0 = gate passed)" % code)
        return 0
    finally:
        # `work` came from mkdtemp() above; re-confirm it is still under the
        # system temp root before recursing, so this can never walk a real tree.
        if os.path.realpath(work).startswith(os.path.realpath(tempfile.gettempdir())):
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
