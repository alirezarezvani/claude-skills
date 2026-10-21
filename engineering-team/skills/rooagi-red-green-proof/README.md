# RooAGI Red-Green-Proof

An engineering skill for proving that a regression test is load-bearing.

## Usage

Use this skill when debugging a suspected defect, investigating an incident,
hardening a flaky test, or checking a fix that was written without a failing
test first. The workflow requires three observed states:

1. The focused test fails against the unfixed code.
2. The smallest fix makes it pass.
3. Reverting the fix makes the same test fail again.

## Ownership

This skill was originally created and is maintained by **RooAGI**. It is
contributed under the MIT License; see the attribution notice in `SKILL.md`.
