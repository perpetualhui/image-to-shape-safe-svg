#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
SKILLS_DEST="${CODEX_HOME_DIR}/skills"
SKILL_NAME="image-to-shape-safe-svg"
DEST="${SKILLS_DEST}/${SKILL_NAME}"

if [[ ! -f "${REPO_ROOT}/SKILL.md" ]]; then
  echo "No SKILL.md found at ${REPO_ROOT}; this script must be run from the skill repository." >&2
  exit 1
fi

mkdir -p "${SKILLS_DEST}"
rm -rf "${DEST}"
mkdir -p "${DEST}"

rsync -a \
  --exclude '.git/' \
  --exclude '.pytest_cache/' \
  --exclude 'svg_shape_safe/' \
  --exclude '__pycache__/' \
  "${REPO_ROOT}/" "${DEST}/"

echo "Installed ${SKILL_NAME} -> ${DEST}"
echo "Restart Codex to pick up new skills."
