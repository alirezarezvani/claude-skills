# Examples

Three input/output pairs, one per deal type, showing what the skill produces.
Each `output.md` is a validated run from the eval suite (iteration 5, the run
that cleared the PR gate) with the eval-harness header removed — the analysis
itself is unedited.

| Folder | Deal type | Input | Verdict |
|---|---|---|---|
| `equity-syndication/` | Value-add multifamily syndication | Full offering summary | Pursue with conditions (financing-story cluster) |
| `hard-money-fund/` | Senior-secured bridge loan fund | Platform-style listing | Pursue (well-disclosed; no RED fired) |
| `private-credit-fund/` | Diversified BDC-style credit fund | Fund summary | Pursue with conditions (structure clears every screen) |

All three land on **Pursue** or **Pursue with conditions** — not because the
skill is agreeable, but because these are the *sound* deals in the suite. The eval suite
also exercises the Pass and Pass-as-presented paths (packed red flags, sparse
solicitations, aggressive development pro formas); those live in `evals/`, not
here, because the shipping examples are meant to show a full, clean analysis
end-to-end. The verdicts differ in their **conditions** and **biggest swing
factor**, which is where the LP lens does its work.
