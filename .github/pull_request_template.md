# Pull Request

## Description

**What does this PR do?**

A clear and concise description of the changes.

## Type of Change

Select the type of change:
- [ ] New skill addition
- [ ] Skill enhancement/improvement
- [ ] Bug fix
- [ ] Documentation update
- [ ] Python script improvement
- [ ] Refactoring/optimization
- [ ] Other (specify)

## Related Issue

Fixes #(issue number)

Or: Related to #(issue number)

---

## Changes Made

### Skills Added/Modified

**Skill Name(s):**
-

**What Changed:**
- Added: (new capabilities, scripts, references)
- Modified: (what was changed and why)
- Removed: (what was deprecated/removed and why)

### Python Scripts

**New Scripts:**
- `script_name.py` - Purpose and functionality

**Modified Scripts:**
- `existing_script.py` - Changes made

### Documentation

**Files Updated:**
- README.md - (what sections)
- SKILL.md - (what changed)
- Reference files - (which ones)

---

## Testing

### Testing Performed

- [ ] Tested with Claude AI (uploaded SKILL.md and verified activation)
- [ ] Tested with Claude Code (loaded skill and ran workflows)
- [ ] All Python scripts run without errors
- [ ] Ran scripts with `--help` flag
- [ ] Tested JSON output (if applicable)
- [ ] All reference links work
- [ ] No broken relative paths

### Test Results

**Claude Activation:**
- [ ] Skill activates when appropriate
- [ ] Description triggers correctly
- [ ] Keywords help discovery

**Python Scripts:**
```bash
# Commands run for testing
python scripts/tool.py --help
python scripts/tool.py test-input.txt
```

**Results:**
```
[Paste test output or describe results]
```

---

## Quality Checklist

### SKILL.md Quality

- [ ] YAML frontmatter is valid
- [ ] `name` matches directory name
- [ ] `description` includes what, when, and keyword triggers
- [ ] `license: MIT` included
- [ ] `metadata` section complete (version, author, category, domain)
- [ ] Keywords section added
- [ ] SKILL.md length <200 lines (or justified if longer)
- [ ] Clear quick start section
- [ ] Core workflows documented
- [ ] Examples included

### Python Scripts Quality (if applicable)

- [ ] Production-ready code (not placeholders)
- [ ] CLI with `--help` support
- [ ] Proper error handling
- [ ] Clear docstrings
- [ ] Type hints used
- [ ] Standard library preferred
- [ ] Dependencies documented
- [ ] No hardcoded paths or credentials

### Documentation Quality

- [ ] All links work (no 404s)
- [ ] Markdown formatting correct
- [ ] No typos or grammar errors
- [ ] Code blocks have language specified
- [ ] Examples are realistic and complete
- [ ] Screenshots included where helpful

### Repository Integration

- [ ] Domain-specific README.md updated (if new skill)
- [ ] Main README.md updated (if new domain or major feature)
- [ ] CLAUDE.md updated (if changes affect development)
- [ ] CHANGELOG.md updated (in Unreleased section)

---

## ROI & Value

**Estimated Value of This Contribution:**

**Time Savings:**
- Hours saved per month per user: (estimate)
- Number of potential users: (estimate)

**Quality Improvements:**
- Specific quality gains: (describe)
- Measurable improvements: (quantify if possible)

**Why This Matters:**
Brief explanation of the business/user value.

---

## Screenshots

If applicable, add screenshots to help explain your changes.

---

## Additional Notes

Any other information reviewers should know:
- Implementation decisions made
- Alternative approaches considered
- Known limitations
- Future enhancement ideas

---

## Contributor Checklist

**Before Submitting:**
- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have followed the skill creation guidelines
- [ ] I have tested thoroughly
- [ ] I have updated all relevant documentation
- [ ] I have added my changes to CHANGELOG.md (Unreleased section)
- [ ] My code follows the repository's style guidelines
- [ ] All new Python scripts are production-ready
- [ ] I agree to the MIT License for my contributions

---

**Thank you for contributing to Claude Skills Library!** 🚀

Your contribution helps make world-class expertise accessible to everyone through Claude AI.
