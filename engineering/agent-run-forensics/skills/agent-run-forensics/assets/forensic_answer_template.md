# Answer template: a question about a past run

**Run:** `<session id>` (`<harness>`, `<start> -> <end>`), source `<path>`

**Answer (recorded):** One or two sentences, each citing a step.
> Step 9 ran `sed -i '...; s/timeout: 30/timeout: 5/' config.yaml` (exit 0). Nothing
> else in the run wrote config.yaml.

**Likely cause (inferred, with rule):**
> It followed the failed test at step 7 (retry-after-failure). The agent's own note
> at the time: "The test expects 3 retries; the config says 0. Setting it." The
> timeout change is not mentioned anywhere in the run.

**Not in the trace:** what the recording cannot answer (e.g. whether this config
was deployed).

**Correction, if an earlier account was wrong:** what was said, what the steps show.
