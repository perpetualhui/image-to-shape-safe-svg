# Repository-local Codex skill

This repository is the `image-to-shape-safe-svg` Codex skill. Keeping the skill files at the repository root makes the GitHub repository layout match the installable skill layout, while still allowing the skill to be copied into a Codex environment without fetching it again.

## Included skill

- `image-to-shape-safe-svg`: converts or matches image/icon inputs into shape-safe SVG assets and includes validation helpers.

## Install this repository into Codex

From the repository root, run:

```bash
./scripts/install-local-skills.sh
```

The script copies this repository into:

```text
${CODEX_HOME:-$HOME/.codex}/skills/image-to-shape-safe-svg
```

After the script finishes, restart Codex so the newly installed skill is loaded.

## Use in Codex web

Codex web checks out this repository into a cloud environment and can run setup scripts before the agent phase. To use this repository-local skill in Codex web:

This guidance follows the official Codex docs for Agent Skills, Codex web cloud tasks, cloud environment setup scripts, and `AGENTS.md` repository instructions. See `references/codex-web-workflow.md` for the detailed source map.

1. Keep `SKILL.md`, `references/`, `tools/`, `assets/`, and `AGENTS.md` committed at the repository root.
2. Add `./scripts/install-local-skills.sh` to the Codex web environment setup if you want this repository copied into `${CODEX_HOME:-$HOME/.codex}/skills/image-to-shape-safe-svg`.
3. Restart Codex when you need the skill to appear in the standard skills list.
4. If restart is not possible during a cloud task, ask Codex to read `SKILL.md` directly.

Suggested Codex web task prompt:

```text
Use the repository-local image-to-shape-safe-svg skill. Read AGENTS.md, then read SKILL.md and references/codex-web-workflow.md. Build or update the web upload-to-SVG workflow and validate generated SVG files with the bundled validator.
```

## Update from GitHub

To refresh a local checkout from GitHub, run:

```bash
git pull --ff-only origin main
./scripts/install-local-skills.sh
```

Then restart Codex if you need the refreshed skill to appear in the standard skills list.

## Add this skill to another repository

If another project wants to vendor this skill locally, copy this repository into that project under `skills/image-to-shape-safe-svg/`, or add it as a Git submodule. In that project, make sure its `AGENTS.md` points Codex to the vendored `SKILL.md` and validation tools.

## Notes for web adaptation

Keeping the skill in the repo makes the prompt instructions and helper tools versioned with the web project. The web app still needs a backend route or job runner to call tools safely, especially for file uploads, image generation, SVG validation, and downloadable artifacts.
