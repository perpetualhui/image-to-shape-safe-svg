# Codex web workflow for image-to-shape-safe-svg

Use this reference when working in Codex web/cloud or when adapting this skill for a browser-based product.


## Official Codex documentation basis

This workflow is based on these OpenAI Codex documentation points:

- Agent Skills: skills are reusable workflow directories with `SKILL.md` and optional `scripts/`, `references/`, `assets/`, and `agents/` resources. See https://developers.openai.com/codex/skills.
- Codex web: cloud tasks check out the repository, run in their own cloud environment, and can create pull requests from the work. See https://developers.openai.com/codex/cloud.
- Cloud environments: setup scripts run before the agent phase; the agent then edits files, runs terminal checks, and uses `AGENTS.md` when present. See https://developers.openai.com/codex/cloud/environments.
- AGENTS.md: repository guidance is discovered from the project tree and loaded before Codex works. See https://developers.openai.com/codex/guides/agents-md.
- In-app browser: Codex can preview local unauthenticated routes and use browser comments for scoped web-app feedback. See https://developers.openai.com/codex/app/browser.
- Agent internet access: agent-phase internet is off by default in Codex web and should be enabled narrowly only when needed. See https://developers.openai.com/codex/cloud/internet-access.

## What Codex web can do for this skill

Codex web runs tasks in a cloud environment where it can check out the repository, run setup scripts, edit files, run terminal checks, and return a diff or pull request. This makes it a good fit for maintaining this skill, adding validators, building web adapters, and generating repository artifacts from uploaded sample files.

The official Codex skills documentation says a skill is a directory with `SKILL.md` plus optional `scripts/`, `references/`, `assets/`, and `agents/` resources. This repository follows that shape at the repository root.

## Loading the skill in Codex web

Codex web may not automatically treat a checked-out repository as a globally installed skill. For reliable use in this repository:

1. Ask Codex to read `AGENTS.md` and `SKILL.md` before converting or adapting images.
2. If you want the skill to appear in the normal skills list, run `./scripts/install-local-skills.sh` and restart Codex.
3. If restarting is not practical inside a cloud task, use the repository-local `SKILL.md`, references, tools, and assets directly.

Recommended prompt:

```text
Use the repository-local image-to-shape-safe-svg skill. Read AGENTS.md, then read SKILL.md and references/codex-web-workflow.md. Adapt the web workflow so users can upload an image and download a validated shape-safe SVG.
```

## Codex web environment setup

For cloud tasks, configure the environment setup script to install only the dependencies needed for validation and previews. Keep setup deterministic and avoid downloading the skill from GitHub because the skill is already the repository being checked out.

Suggested setup commands:

```bash
python -m pip install --upgrade pip
python -m pip install pytest cairosvg pillow
./scripts/install-local-skills.sh
```

Notes:

- Setup scripts run before the agent starts, so they are the right place to install Python packages or copy local skills.
- If the cloud task needs external downloads during the agent phase, enable agent internet access for the environment and keep the allowlist narrow.
- Secrets are not available to the agent phase in Codex cloud. Do not design this skill to require runtime secrets for SVG validation.

## Web product adaptation pattern

A browser product should not expose raw filesystem paths or API keys. Use a backend job pipeline:

1. `POST /api/uploads`: receive PNG/JPG/WebP/PDF/PPTX inputs and store them as artifacts.
2. `POST /api/svg-jobs`: create an image-to-shape-safe-SVG conversion job.
3. Worker reads the input artifact and uses this skill's reconstruction rules.
4. Worker writes output to `svg_shape_safe/<job-id>/`.
5. Worker runs `tools/validate_shape_safe_svg.py` on every SVG.
6. `GET /api/svg-jobs/:id`: return status, preview URL, validation summary, and download URL.
7. `GET /api/artifacts/:id/download`: download the final SVG or ZIP.

## Uploaded file handling

Treat uploaded files as untrusted input:

- Limit file size and MIME type.
- Store source files outside the public web root.
- Generate sanitized preview images.
- Never embed uploaded raster images into the final SVG.
- Strip or avoid active SVG content such as scripts, event handlers, external links, and `foreignObject`.

## Output requirements for web downloads

Every web-generated SVG should still satisfy the skill's hard validation targets:

- no embedded `<image>` nodes
- no `data-icon` placeholders
- no transforms
- no marker arrowheads
- no `foreignObject`
- no disallowed `tspan`

Return a machine-readable validation report with each downloadable artifact so the UI can show whether the SVG is Office/PPT shape-safe.

## Preview and iteration in Codex app

When adapting a real web app, use the Codex in-app browser to preview local unauthenticated routes, inspect rendered upload/download flows, and leave comments on precise UI areas. Keep browser tasks scoped to one route or visual state at a time.

## Minimal Codex web task templates

### Build the upload-to-SVG UI

```text
Use the repository-local image-to-shape-safe-svg skill. Build a web page where users upload a PNG/JPG, start a conversion job, preview the generated shape-safe SVG, see validation results, and download the SVG. Keep API keys server-side and validate output with tools/validate_shape_safe_svg.py.
```

### Convert sample files in the repo

```text
Use the repository-local image-to-shape-safe-svg skill. Convert the sample images in <folder> into shape-safe SVG files under svg_shape_safe/. Ask whether to preserve all source icons before final conversion. Validate every SVG and report the validation metrics.
```

### Review a generated SVG

```text
Use the repository-local image-to-shape-safe-svg skill. Review <file.svg> for Office/PPT shape-safety, run the validator, fix any forbidden SVG features, and preserve the visual hierarchy.
```
