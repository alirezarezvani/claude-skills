#!/usr/bin/env bash
# review-new-skills.sh — Run Tessl + internal auditors on new/changed skills
#
# Usage:
#   ./scripts/review-new-skills.sh                    # Review all changed skills (vs dev)
#   ./scripts/review-new-skills.sh engineering/behuman # Review specific skill
#   ./scripts/review-new-skills.sh --all              # Review ALL skills (slow)
#   ./scripts/review-new-skills.sh --threshold 80     # Set minimum score (default: 70)

set -euo pipefail

THRESHOLD="${THRESHOLD:-70}"
SKILL_DIRS=()
MODE="changed"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      MODE="all"
      shift
      ;;
    --threshold)
      THRESHOLD="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [--all] [--threshold N] [skill-dir ...]"
      echo ""
      echo "Options:"
      echo "  --all          Review all skills (not just changed ones)"
      echo "  --threshold N  Minimum Tessl score to pass (default: 70)"
      echo "  skill-dir      Specific skill directory to review"
      exit 0
      ;;
    *)
      SKILL_DIRS+=("$1")
      MODE="specific"
      shift
      ;;
  esac
done

# Determine which skills to review
if [ "$MODE" = "all" ]; then
  while IFS= read -r f; do
    dir=$(dirname "$f")
    SKILL_DIRS+=("$dir")
  done < <(find . -name SKILL.md -not -path './.codex/*' -not -path './.gemini/*' -not -path './docs/*' -not -path './eval-workspace/*' -not -path './medium/*' -not -path '*/assets/*' -maxdepth 3 | sed 's|^\./||' | sort)
elif [ "$MODE" = "changed" ] && [ ${#SKILL_DIRS[@]} -eq 0 ]; then
  echo "Detecting changed skills vs origin/dev..."
  CHANGED=$(git diff --name-only origin/dev...HEAD 2>/dev/null || git diff --name-only HEAD~1 2>/dev/null || echo "")
  if [ -z "$CHANGED" ]; then
    echo "No changes detected. Use --all or specify a skill directory."
    exit 0
  fi
  SEEN=()
  while IFS= read -r file; do
    dir=$(echo "$file" | cut -d'/' -f1-2)
    case "$dir" in
      .github/*|.claude/*|.codex/*|.gemini/*|docs/*|scripts/*|commands/*|standards/*|eval-workspace/*|medium/*) continue ;;
    esac
    if [ -f "$dir/SKILL.md" ] && [[ ! " ${SEEN[*]:-} " =~ " $dir " ]]; then
      SKILL_DIRS+=("$dir")
      SEEN+=("$dir")
    fi
  done <<< "$CHANGED"
fi

if [ ${#SKILL_DIRS[@]} -eq 0 ]; then
  echo "No skills to review."
  exit 0
fi

echo "================================================================"
echo "  SKILL QUALITY REVIEW"
echo "  Threshold: ${THRESHOLD}/100"
echo "  Skills: ${#SKILL_DIRS[@]}"
echo "================================================================"
echo ""

PASS_COUNT=0
FAIL_COUNT=0
RESULTS=()

for skill_dir in "${SKILL_DIRS[@]}"; do
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    echo "⏭  $skill_dir — no SKILL.md, skipping"
    continue
  fi

  echo "━━━ $skill_dir ━━━"

  # 1. Tessl review
  TESSL_SCORE=0
  if command -v tessl &>/dev/null; then
    TESSL_JSON=$(tessl skill review "$skill_dir" --json 2>/dev/null || echo '{}')
    TESSL_SCORE=$(echo "$TESSL_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('review', {}).get('reviewScore', 0))
except:
    print(0)
" 2>/dev/null || echo "0")
    TESSL_DESC=$(echo "$TESSL_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(round(d.get('descriptionJudge', {}).get('normalizedScore', 0) * 100))
except:
    print(0)
" 2>/dev/null || echo "0")
    TESSL_CONTENT=$(echo "$TESSL_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(round(d.get('contentJudge', {}).get('normalizedScore', 0) * 100))
except:
    print(0)
" 2>/dev/null || echo "0")

    if [ "$TESSL_SCORE" -ge "$THRESHOLD" ]; then
      echo "  ✅ Tessl:    ${TESSL_SCORE}/100 (desc: ${TESSL_DESC}%, content: ${TESSL_CONTENT}%)"
    else
      echo "  ⚠️  Tessl:    ${TESSL_SCORE}/100 (desc: ${TESSL_DESC}%, content: ${TESSL_CONTENT}%) — BELOW THRESHOLD"
    fi
  else
    echo "  ⏭  Tessl:    not installed (npm install -g tessl)"
  fi

  # 2. Structure validation
  STRUCT_SCORE=$(python3 engineering/skill-tester/scripts/skill_validator.py "$skill_dir" --json 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'{d[\"overall_score\"]}/{d[\"compliance_level\"]}')
except:
    print('0/ERROR')
" 2>/dev/null || echo "0/ERROR")
  echo "  📐 Structure: $STRUCT_SCORE"

  # 3. Script testing
  if [ -d "$skill_dir/scripts" ] && ls "$skill_dir/scripts/"*.py >/dev/null 2>&1; then
    SCRIPT_RESULT=$(python3 engineering/skill-tester/scripts/script_tester.py "$skill_dir" --json 2>&1 | python3 -c "
import sys, json
text = sys.stdin.read()
try:
    start = text.index('{')
    d = json.loads(text[start:])
    print(f'{d[\"summary\"][\"passed\"]}/{d[\"summary\"][\"total_scripts\"]} PASS')
except:
    print('ERROR')
" 2>/dev/null || echo "ERROR")
    echo "  🧪 Scripts:  $SCRIPT_RESULT"
  fi

  # 4. Security audit
  SEC_RESULT=$(python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py "$skill_dir" --strict --json 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    c = d['summary']['critical']
    h = d['summary']['high']
    print(f'{d[\"verdict\"]} (critical:{c}, high:{h})')
except:
    print('ERROR')
" 2>/dev/null || echo "ERROR")
  echo "  🔒 Security: $SEC_RESULT"

  # Verdict
  if [ "$TESSL_SCORE" -ge "$THRESHOLD" ]; then
    PASS_COUNT=$((PASS_COUNT + 1))
    RESULTS+=("✅ $skill_dir: ${TESSL_SCORE}/100")
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    RESULTS+=("⚠️  $skill_dir: ${TESSL_SCORE}/100 — below ${THRESHOLD}")
  fi

  echo ""
done

echo "================================================================"
echo "  SUMMARY"
echo "================================================================"
for r in "${RESULTS[@]}"; do
  echo "  $r"
done
echo ""
echo "  Pass: $PASS_COUNT | Below threshold: $FAIL_COUNT"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
