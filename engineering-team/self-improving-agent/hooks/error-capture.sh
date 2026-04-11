#!/bin/bash
# Self-Improving Agent — Error Capture Hook
# Fires on PostToolUse (Bash) to detect command failures.
# Zero output on success — only captures when errors are detected.
#
# When installed via `/plugin install self-improving-agent@claude-code-skills`
# this hook is registered automatically from the plugin's hooks.json. No
# manual wiring is required.
#
# If you need to wire it up manually, use ${CLAUDE_PLUGIN_ROOT} — a relative
# path like ./hooks/error-capture.sh resolves against your current working
# directory, not the plugin root, and will silently fail in every session
# started outside the plugin install dir.
#
#   .claude/settings.json:
#   {
#     "hooks": {
#       "PostToolUse": [{
#         "matcher": "Bash",
#         "hooks": [{
#           "type": "command",
#           "command": "${CLAUDE_PLUGIN_ROOT}/hooks/error-capture.sh"
#         }]
#       }]
#     }
#   }

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Exit silently if no output or empty
[ -z "$OUTPUT" ] && exit 0

# Error patterns — ordered by specificity
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "FATAL:"
    "fatal:"
    "FAILED"
    "failed"
    "command not found"
    "No such file or directory"
    "Permission denied"
    "Module not found"
    "ModuleNotFoundError"
    "ImportError"
    "SyntaxError"
    "TypeError"
    "ReferenceError"
    "Cannot find module"
    "ENOENT"
    "EACCES"
    "ECONNREFUSED"
    "ETIMEDOUT"
    "npm ERR!"
    "pnpm ERR!"
    "Traceback (most recent call last)"
    "panic:"
    "segmentation fault"
    "core dumped"
    "exit code"
    "non-zero exit"
    "Build failed"
    "Compilation failed"
    "Test failed"
)

# False positive exclusions — don't trigger on these
EXCLUSIONS=(
    "error-capture"       # Don't trigger on ourselves
    "error_handler"       # Code that handles errors
    "errorHandler"
    "error.log"           # Log file references
    "console.error"       # Code that logs errors
    "catch (error"        # Error handling code
    "catch (err"
    ".error("             # Logger calls
    "no error"            # Absence of error
    "without error"
    "error-free"
)

# Check exclusions first
for excl in "${EXCLUSIONS[@]}"; do
    if [[ "$OUTPUT" == *"$excl"* ]]; then
        exit 0
    fi
done

# Check for error patterns
contains_error=false
matched_pattern=""
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        matched_pattern="$pattern"
        break
    fi
done

# Exit silently if no error
[ "$contains_error" = false ] && exit 0

# Extract relevant error context (first 5 lines containing the pattern)
error_context=$(echo "$OUTPUT" | grep -i -m 5 "$matched_pattern" | head -5)

# Output a concise reminder — ~40 tokens
cat << EOF
<error-detected>
Command error detected (pattern: "$matched_pattern").
If this was unexpected or required investigation to fix, save the solution:
  /si:remember "explanation of what went wrong and the fix"
Or if this is a known pattern, check: /si:review
Context: $(echo "$error_context" | head -2 | tr '\n' ' ' | cut -c1-200)
</error-detected>
EOF
