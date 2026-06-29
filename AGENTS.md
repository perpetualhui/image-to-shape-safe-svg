# Repository guidance for Codex

## Local skill in this repo

This repository is the `image-to-shape-safe-svg` Codex skill. When a task mentions image-to-SVG conversion, shape-safe SVG, editable PowerPoint/Office SVG, web upload-to-SVG workflows, or `image-to-shape-safe-svg`, read `SKILL.md` before planning the work.

For Codex web/cloud tasks, do not assume this repository has already been installed into the global Codex skills directory. If the task requires the skill behavior and it is not available in the initial skill list, use the repository-local files directly:

1. Read `SKILL.md`.
2. Read `references/codex-web-workflow.md` for Codex web usage.
3. Read `references/web-workflow.md` for browser app implementation details.
4. Run validation with `python tools/validate_shape_safe_svg.py <svg>` when producing SVG output.

If the environment should install this repository into Codex home, run:

```bash
./scripts/install-local-skills.sh
```

Restart Codex after installation when the goal is to make the skill appear in the normal skills list.
