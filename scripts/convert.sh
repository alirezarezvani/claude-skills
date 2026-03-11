#!/usr/bin/env bash
# Usage:
#   ./scripts/convert.sh [--tool <name>] [--out <dir>] [--help]
#
# Tools: antigravity, cursor, aider, kilocode, windsurf, opencode, augment, all
# Default: all

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOOL="all"
OUT_BASE="${REPO_ROOT}/integrations"
TODAY="$(date +%F)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

ok() {
  echo -e "${GREEN}[OK]${NC} $*"
}

warn() {
  echo -e "${YELLOW}[!!]${NC} $*"
}

err() {
  echo -e "${RED}[ERR]${NC} $*" >&2
}

info() {
  echo -e "${BLUE}[*]${NC} $*"
}

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/convert.sh [--tool <name>] [--out <dir>] [--help]

Tools:
  antigravity, cursor, aider, kilocode, windsurf, opencode, augment, all

Defaults:
  --tool all
  --out  <repo-root>/integrations
USAGE
}

is_valid_tool() {
  case "$1" in
    antigravity|cursor|aider|kilocode|windsurf|opencode|augment|all) return 0 ;;
    *) return 1 ;;
  esac
}

yaml_unquote() {
  local value="$1"
  value="${value#\"}"
  value="${value%\"}"
  value="${value#\'}"
  value="${value%\'}"
  printf '%s' "$value"
}

yaml_quote() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '"%s"' "$value"
}

init_count_vars() {
  converted_antigravity=0
  converted_cursor=0
  converted_aider=0
  converted_kilocode=0
  converted_windsurf=0
  converted_opencode=0
  converted_augment=0

  skipped_antigravity=0
  skipped_cursor=0
  skipped_aider=0
  skipped_kilocode=0
  skipped_windsurf=0
  skipped_opencode=0
  skipped_augment=0
}

inc_converted() {
  local t="$1"
  case "$t" in
    antigravity) converted_antigravity=$((converted_antigravity + 1)) ;;
    cursor) converted_cursor=$((converted_cursor + 1)) ;;
    aider) converted_aider=$((converted_aider + 1)) ;;
    kilocode) converted_kilocode=$((converted_kilocode + 1)) ;;
    windsurf) converted_windsurf=$((converted_windsurf + 1)) ;;
    opencode) converted_opencode=$((converted_opencode + 1)) ;;
    augment) converted_augment=$((converted_augment + 1)) ;;
  esac
}

inc_skipped() {
  local t="$1"
  case "$t" in
    antigravity) skipped_antigravity=$((skipped_antigravity + 1)) ;;
    cursor) skipped_cursor=$((skipped_cursor + 1)) ;;
    aider) skipped_aider=$((skipped_aider + 1)) ;;
    kilocode) skipped_kilocode=$((skipped_kilocode + 1)) ;;
    windsurf) skipped_windsurf=$((skipped_windsurf + 1)) ;;
    opencode) skipped_opencode=$((skipped_opencode + 1)) ;;
    augment) skipped_augment=$((skipped_augment + 1)) ;;
  esac
}

get_converted() {
  local t="$1"
  case "$t" in
    antigravity) echo "$converted_antigravity" ;;
    cursor) echo "$converted_cursor" ;;
    aider) echo "$converted_aider" ;;
    kilocode) echo "$converted_kilocode" ;;
    windsurf) echo "$converted_windsurf" ;;
    opencode) echo "$converted_opencode" ;;
    augment) echo "$converted_augment" ;;
  esac
}

get_skipped() {
  local t="$1"
  case "$t" in
    antigravity) echo "$skipped_antigravity" ;;
    cursor) echo "$skipped_cursor" ;;
    aider) echo "$skipped_aider" ;;
    kilocode) echo "$skipped_kilocode" ;;
    windsurf) echo "$skipped_windsurf" ;;
    opencode) echo "$skipped_opencode" ;;
    augment) echo "$skipped_augment" ;;
  esac
}

# Prints frontmatter fields as: name<TAB>description
extract_frontmatter() {
  local file="$1"
  awk '
    BEGIN {
      in_fm = 0
      name = ""
      desc = ""
      in_desc_block = 0
    }

    function ltrim(s) {
      sub(/^[[:space:]]+/, "", s)
      return s
    }

    function rtrim(s) {
      sub(/[[:space:]]+$/, "", s)
      return s
    }

    function trim(s) {
      return rtrim(ltrim(s))
    }

    function dequote(s, first, last) {
      s = trim(s)
      first = substr(s, 1, 1)
      last = substr(s, length(s), 1)
      if ((first == "\"" && last == "\"") || (first == "\047" && last == "\047")) {
        s = substr(s, 2, length(s) - 2)
        if (first == "\"") {
          gsub(/\\\\/, "\\", s)
          gsub(/\\"/, "\"", s)
        } else {
          gsub(/\047\047/, "\047", s)
        }
      }
      return s
    }

    function append_desc(chunk) {
      chunk = trim(chunk)
      if (chunk == "") return
      if (desc == "") {
        desc = chunk
      } else {
        desc = desc " " chunk
      }
    }

    NR == 1 {
      if ($0 == "---") {
        in_fm = 1
        next
      }
      next
    }

    in_fm == 1 {
      if ($0 == "---") {
        in_fm = 0
        next
      }

      if (in_desc_block == 1) {
        if ($0 ~ /^[[:space:]]+/ || $0 == "") {
          line = $0
          sub(/^[[:space:]]+/, "", line)
          append_desc(line)
          next
        }
        in_desc_block = 0
      }

      if ($0 ~ /^name:[[:space:]]*/) {
        line = $0
        sub(/^name:[[:space:]]*/, "", line)
        name = dequote(line)
        next
      }

      if ($0 ~ /^description:[[:space:]]*/) {
        line = $0
        sub(/^description:[[:space:]]*/, "", line)
        line = trim(line)

        if (line ~ /^>[+-]?$/ || line ~ /^\|[+-]?$/) {
          in_desc_block = 1
          next
        }

        desc = dequote(line)
        next
      }

      next
    }

    END {
      printf "%s\t%s\n", trim(name), trim(desc)
    }
  ' "$file"
}

extract_body() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0 }

    NR == 1 {
      if ($0 == "---") {
        in_fm = 1
        next
      }
      print
      next
    }

    in_fm == 1 {
      if ($0 == "---") {
        in_fm = 0
        next
      }
      next
    }

    { print }
  ' "$file"
}

copy_supporting_dirs() {
  local src_dir="$1"
  local dst_dir="$2"
  local d
  for d in scripts references templates; do
    if [[ -d "${src_dir}/${d}" ]]; then
      cp -R "${src_dir}/${d}" "${dst_dir}/${d}"
    fi
  done
}

append_aider_skill() {
  local name="$1"
  local description="$2"
  local body_file="$3"

  {
    echo "---"
    echo
    echo "## ${name}"
    echo "> ${description}"
    echo
    cat "$body_file"
    echo
  } >> "${AIDER_FILE}"
}

tool_title() {
  case "$1" in
    antigravity) echo "Antigravity" ;;
    cursor) echo "Cursor" ;;
    aider) echo "Aider" ;;
    kilocode) echo "Kilo Code" ;;
    windsurf) echo "Windsurf" ;;
    opencode) echo "OpenCode" ;;
    augment) echo "Augment" ;;
  esac
}

write_tool_readme() {
  local tool="$1"
  local count="$2"
  local out_dir="${OUT_BASE}/${tool}"

  local format_line=""
  local manual_install=""
  local script_install="./scripts/install.sh --tool ${tool}"
  local verify_step=""
  local update_step=""

  case "$tool" in
    antigravity)
      format_line='Directory skill bundles: `SKILL.md` with Antigravity frontmatter (`risk`, `source`, `date_added`) plus copied `scripts/`, `references/`, `templates/` when present.'
      manual_install='Copy each folder from `integrations/antigravity/<skill-name>/` to `~/.gemini/antigravity/skills/<skill-name>/`.'
      verify_step='Run `find ~/.gemini/antigravity/skills -name "SKILL.md" | wc -l` and confirm the count, then check your Gemini/Antigravity skill list.'
      update_step='Re-run `./scripts/convert.sh --tool antigravity` and then reinstall with `./scripts/install.sh --tool antigravity`.'
      ;;
    cursor)
      format_line='Flat Cursor rules: `rules/<skill-name>.mdc` with Cursor-compatible frontmatter (`description`, `globs`, `alwaysApply`).'
      manual_install='Copy `integrations/cursor/rules/*.mdc` into your project `.cursor/rules/` directory.'
      verify_step='Open Cursor rules panel or run `find .cursor/rules -name "*.mdc" | wc -l` in your project.'
      update_step='Re-run `./scripts/convert.sh --tool cursor` and then reinstall with `./scripts/install.sh --tool cursor --target <project-dir>`.'
      ;;
    aider)
      format_line='Single conventions file: `CONVENTIONS.md` concatenating all skills with separators and per-skill sections.'
      manual_install='Copy `integrations/aider/CONVENTIONS.md` into your project root.'
      verify_step='Run `aider --read CONVENTIONS.md` and confirm sections load (search for `## <skill-name>` entries).'
      update_step='Re-run `./scripts/convert.sh --tool aider` and reinstall with `./scripts/install.sh --tool aider --target <project-dir>`.'
      ;;
    kilocode)
      format_line='Flat markdown rules: `rules/<skill-name>.md` with a title/description header and no frontmatter.'
      manual_install='Copy `integrations/kilocode/rules/*.md` into your project `.kilocode/rules/` directory.'
      verify_step='Run `find .kilocode/rules -name "*.md" | wc -l` in your project and confirm expected count.'
      update_step='Re-run `./scripts/convert.sh --tool kilocode` and reinstall with `./scripts/install.sh --tool kilocode --target <project-dir>`.'
      ;;
    windsurf)
      format_line='Directory skill bundles: `skills/<skill-name>/SKILL.md` using Windsurf-compatible SKILL frontmatter (`name`, `description`) plus copied support folders.'
      manual_install='Copy each folder from `integrations/windsurf/skills/<skill-name>/` to `.windsurf/skills/<skill-name>/` in your project.'
      verify_step='Run `find .windsurf/skills -name "SKILL.md" | wc -l` and verify skills are listed in Windsurf.'
      update_step='Re-run `./scripts/convert.sh --tool windsurf` and reinstall with `./scripts/install.sh --tool windsurf --target <project-dir>`.'
      ;;
    opencode)
      format_line='Directory skill bundles: `skills/<skill-name>/SKILL.md` with `compatibility: opencode` plus copied support folders.'
      manual_install='Copy each folder from `integrations/opencode/skills/<skill-name>/` to `.opencode/skills/<skill-name>/` in your project.'
      verify_step='Run `find .opencode/skills -name "SKILL.md" | wc -l` and confirm OpenCode shows installed skills.'
      update_step='Re-run `./scripts/convert.sh --tool opencode` and reinstall with `./scripts/install.sh --tool opencode --target <project-dir>`.'
      ;;
    augment)
      format_line='Flat Augment rules: `rules/<skill-name>.md` with Augment frontmatter (`type: auto`, `description`).'
      manual_install='Copy `integrations/augment/rules/*.md` into your project `.augment/rules/` directory.'
      verify_step='Run `find .augment/rules -name "*.md" | wc -l` and check rules appear in Augment.'
      update_step='Re-run `./scripts/convert.sh --tool augment` and reinstall with `./scripts/install.sh --tool augment --target <project-dir>`.'
      ;;
  esac

  {
    printf '# %s Integration\n\n' "$(tool_title "$tool")"
    printf '![%s](https://img.shields.io/badge/Integration-%s-0A66C2)\n\n' "$tool" "$tool"
    printf 'This directory contains converted Claude Skills for **%s**.\n\n' "$(tool_title "$tool")"
    printf '## Included Skills\n\n'
    printf -- '- **%s** skills generated from this repository.\n\n' "$count"
    printf '## Format\n\n'
    printf '%s\n\n' "$format_line"
    printf '## Install\n\n'
    printf '### Manual\n\n'
    printf '%s\n\n' "$manual_install"
    printf '### Script\n\n'
    printf '```bash\n'
    printf 'git clone https://github.com/alirezarezvani/claude-skills.git\n'
    printf 'cd claude-skills\n'
    printf '%s\n' "$script_install"
    printf '```\n\n'
    printf '## Verify\n\n'
    printf '%s\n\n' "$verify_step"
    printf '## Update\n\n'
    printf '%s\n\n' "$update_step"
    printf '## Source Repository\n\n'
    printf -- '- https://github.com/alirezarezvani/claude-skills\n'
  } > "${out_dir}/README.md"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      shift 2
      ;;
    --out)
      OUT_BASE="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      err "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if ! is_valid_tool "$TOOL"; then
  err "Invalid --tool value: ${TOOL}"
  usage
  exit 1
fi

TOOLS="antigravity cursor aider kilocode windsurf opencode augment"
if [[ "$TOOL" != "all" ]]; then
  TOOLS="$TOOL"
fi

SKILLS_TMP="$(mktemp)"
(
  cd "$REPO_ROOT"
  find . -mindepth 3 -maxdepth 3 -type f -name 'SKILL.md' -not -path './.git/*' | sort
) > "$SKILLS_TMP"

TOTAL_CANDIDATES="$(wc -l < "$SKILLS_TMP" | tr -d ' ')"
if [[ "$TOTAL_CANDIDATES" -eq 0 ]]; then
  err "No skills found matching */*/SKILL.md"
  rm -f "$SKILLS_TMP"
  exit 1
fi

info "Found ${TOTAL_CANDIDATES} candidate skills"

for t in $TOOLS; do
  rm -rf "${OUT_BASE}/${t}"
  mkdir -p "${OUT_BASE}/${t}"
  if [[ "$t" == "cursor" || "$t" == "kilocode" || "$t" == "augment" ]]; then
    mkdir -p "${OUT_BASE}/${t}/rules"
  fi
  if [[ "$t" == "windsurf" || "$t" == "opencode" ]]; then
    mkdir -p "${OUT_BASE}/${t}/skills"
  fi
  if [[ "$t" == "aider" ]]; then
    AIDER_FILE="${OUT_BASE}/aider/CONVENTIONS.md"
    {
      echo "# Claude Skills — Aider Conventions"
      echo "> Auto-generated from claude-skills. Do not edit manually."
      echo "> Generated: ${TODAY}"
      echo
    } > "$AIDER_FILE"
  fi
  ok "Prepared output directory: ${OUT_BASE}/${t}"
done

init_count_vars

while IFS= read -r rel_path; do
  src="${REPO_ROOT}/${rel_path#./}"
  src_dir="$(dirname "$src")"

  meta="$(extract_frontmatter "$src")"
  name="${meta%%$'\t'*}"
  description="${meta#*$'\t'}"

  name="$(yaml_unquote "$name")"
  description="$(yaml_unquote "$description")"

  if [[ -z "$name" || -z "$description" ]]; then
    for t in $TOOLS; do
      inc_skipped "$t"
    done
    warn "Skipping invalid frontmatter: ${rel_path}"
    continue
  fi

  body_tmp="$(mktemp)"
  extract_body "$src" > "$body_tmp"

  for t in $TOOLS; do
    case "$t" in
      antigravity)
        out_dir="${OUT_BASE}/antigravity/${name}"
        mkdir -p "$out_dir"
        {
          echo "---"
          echo "name: $(yaml_quote "$name")"
          echo "description: $(yaml_quote "$description")"
          echo "risk: low"
          echo "source: community"
          echo "date_added: '${TODAY}'"
          echo "---"
          cat "$body_tmp"
        } > "${out_dir}/SKILL.md"
        copy_supporting_dirs "$src_dir" "$out_dir"
        ;;
      cursor)
        out_file="${OUT_BASE}/cursor/rules/${name}.mdc"
        {
          echo "---"
          echo "description: $(yaml_quote "$description")"
          echo "globs:"
          echo "alwaysApply: false"
          echo "---"
          cat "$body_tmp"
        } > "$out_file"
        ;;
      aider)
        append_aider_skill "$name" "$description" "$body_tmp"
        ;;
      kilocode)
        out_file="${OUT_BASE}/kilocode/rules/${name}.md"
        {
          echo "# ${name}"
          echo "> ${description}"
          echo
          cat "$body_tmp"
        } > "$out_file"
        ;;
      windsurf)
        out_dir="${OUT_BASE}/windsurf/skills/${name}"
        mkdir -p "$out_dir"
        {
          echo "---"
          echo "name: $(yaml_quote "$name")"
          echo "description: $(yaml_quote "$description")"
          echo "---"
          cat "$body_tmp"
        } > "${out_dir}/SKILL.md"
        copy_supporting_dirs "$src_dir" "$out_dir"
        ;;
      opencode)
        out_dir="${OUT_BASE}/opencode/skills/${name}"
        mkdir -p "$out_dir"
        {
          echo "---"
          echo "name: $(yaml_quote "$name")"
          echo "description: $(yaml_quote "$description")"
          echo "compatibility: opencode"
          echo "---"
          cat "$body_tmp"
        } > "${out_dir}/SKILL.md"
        copy_supporting_dirs "$src_dir" "$out_dir"
        ;;
      augment)
        out_file="${OUT_BASE}/augment/rules/${name}.md"
        {
          echo "---"
          echo "type: auto"
          echo "description: $(yaml_quote "$description")"
          echo "---"
          cat "$body_tmp"
        } > "$out_file"
        ;;
      *)
        err "Unhandled tool: ${t}"
        rm -f "$body_tmp" "$SKILLS_TMP"
        exit 1
        ;;
    esac

    inc_converted "$t"
  done

  rm -f "$body_tmp"
  ok "Converted ${name} (${rel_path})"
done < "$SKILLS_TMP"

rm -f "$SKILLS_TMP"

for t in $TOOLS; do
  write_tool_readme "$t" "$(get_converted "$t")"
done

echo
info "Conversion summary"
for t in $TOOLS; do
  echo "  ${t}: $(get_converted "$t") converted, $(get_skipped "$t") skipped"
done

echo
ok "Done"
