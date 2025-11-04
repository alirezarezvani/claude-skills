---
description: Run the local review gate before pushing.
---

Perform a complete review pass:

1. Save work in progress and ensure the working tree is clean except for intentional changes.
2. Install tooling (only first run):
   ```bash
   pip install --upgrade pip
   pip install yamllint==1.35.1 check-jsonschema==0.28.4 safety==3.2.4
   npm install --global markdown-link-check@3.12.2
   ```
3. Lint GitHub workflows:
   ```bash
   yamllint -d '{extends: default, rules: {line-length: {max: 160}}}' .github/workflows
   check-jsonschema --schema github-workflow --base-dir . .github/workflows/*.yml
   ```
4. Python syntax check:
   ```bash
   python -m compileall marketing-skill product-team c-level-advisor engineering-team ra-qm-team
   ```
5. Markdown sanity check:
   ```bash
   markdown-link-check README.md
   ```
6. Optional dependency audit (if `requirements*.txt` present):
   ```bash
   for f in $(find . -name "requirements*.txt" 2>/dev/null); do
       safety check --full-report --file "$f"
   done
   ```
7. Summarize results in the commit template's Testing section. Fix any failures before continuing.
