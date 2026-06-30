# Image To Shape-Safe SVG

Languages: [English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Deprecated for editable PowerPoint reconstruction: use [`image-to-pptx`](../image-to-pptx/) when the target is native editable PPTX text boxes. This skill remains for explicit SVG output only.

Convert slide-like images, screenshots, flowcharts, business diagrams, and infographic pages into editable SVG files that are safer to convert into PowerPoint shapes.

This is a Codex skill for reconstructing visual documents structurally. It does not trace a bitmap. Instead, it rebuilds the page with SVG primitives such as text, paths, lines, polygons, icons, and simple shapes so the output remains easier to edit in Office.

## What It Does

- Reconstructs raster slide screenshots into structured SVG.
- Prioritizes PowerPoint convert-to-shapes compatibility.
- Avoids embedded screenshots, `foreignObject`, SVG transforms, marker-based arrows, and unexpanded icon placeholders.
- Bakes arrowheads as polygons so connectors survive Office conversion.
- Keeps most text as independent SVG text nodes for easier editing.
- Allows limited multi-line explanatory text blocks with a marked `data-text-role="explanatory-block"` exception.
- Includes a bundled semantic icon library with automatic keyword matching.
- Outputs individual SVG files by default; ZIP and multi-page delivery reports require user approval.
- Uses one semantic paragraph per editable text box with a fixed Microsoft YaHei typography scale.
- Reduces decorative icon noise by default and favors numbered circles, dots, pills, color chips, and badges where appropriate.

## Shape-Safe Output Rules

Final SVG files should pass these hard validation targets:

```text
image = 0
data_icon = 0
transform = 0
marker_end = 0
marker_defs = 0
tspan = 0, except approved explanatory blocks
foreign_object = 0
```

The default output is individual standalone SVG files. If a folder is useful, use:

```text
svg_shape_safe/
```

Do not create ZIP archives or multi-page delivery reports unless the user explicitly asks or approves them.

## Repository Layout

```text
.
|-- SKILL.md
|-- config.yaml
|-- agents/
|-- assets/
|   `-- icons/
|-- docs/
|   |-- icon-matching.md
|   |-- map-complexity-policy.md
|   `-- troubleshooting.md
|-- examples/
|   |-- basic_usage.md
|   `-- web_usage.md
|-- references/
|   |-- local-batch-workflow.md
|   `-- web-workflow.md
|-- tests/
|   `-- test_validate_shape_safe_svg.py
`-- tools/
    |-- match_shape_safe_icon.py
    `-- validate_shape_safe_svg.py
```

## Installation

Clone the repository into your Codex skills directory or copy the folder into an existing `.agents/skills` directory:

```bash
git clone https://github.com/perpetualhui/image-to-shape-safe-svg.git
```

If your local Codex setup uses project-scoped skills, place it at:

```text
.agents/skills/image-to-shape-safe-svg/
```

## Usage

In Codex, invoke the skill by name:

```text
Use $image-to-shape-safe-svg to convert these slide screenshots into editable SVG.
Only deliver svg_shape_safe. Make sure icons and arrowheads survive PowerPoint convert-to-shapes.
```

More examples:

```text
Use $image-to-shape-safe-svg to rebuild this process diagram as editable SVG.
Use a balanced icon strategy and replace repeated decorative icons with numbered circles.
```

```text
Use $image-to-shape-safe-svg on these five dashboard screenshots.
Create a preflight summary first, then deliver only SVGs that pass the validator.
```

Icon matching example:

```bash
python tools/match_shape_safe_icon.py "automation workflow" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

This emits expanded SVG primitives from the bundled icon library. The output avoids `<image>`, `transform`, `marker`, `foreignObject`, and `data-icon`.

For local batch work, follow:

```text
references/local-batch-workflow.md
```

For browser or web-app workflows, follow:

```text
references/web-workflow.md
```

## Recommended Workflow

1. Inspect the image dimensions and composition.
2. Create a short preflight note with complexity, icon count, text density risk, layout strategy, visual-model call budget, icon-retention decision status, typography assumptions, and report preference for multi-page jobs.
3. Before conversion, always ask whether the user wants to preserve all source icons or simplify decorative/repeated icons.
4. Ask before generating a multi-page validation/delivery report.
5. Rebuild the page structurally with editable SVG primitives.
6. Use one semantic paragraph per editable text box.
7. Use the fixed typography scale: `24 / 18 / 16 / 14 / 12 / 10 / 8`.
8. Use a small, deliberate icon budget.
9. Draw arrows as lines or paths plus baked polygon arrowheads.
10. Validate the SVG files with the included tool.
11. Render previews and inspect for layout drift, overlap, missing arrowheads, and Office-risky SVG features.

## Validation

Validate a file or a folder:

```bash
python tools/validate_shape_safe_svg.py path/to/svg_shape_safe
```

On Windows, if `python` points to the Microsoft Store launcher, use:

```powershell
py tools\validate_shape_safe_svg.py path\to\svg_shape_safe
```

Print JSON:

```bash
python tools/validate_shape_safe_svg.py --json path/to/svg_shape_safe
```

Run tests when `pytest` is installed:

```bash
python -m pytest tests
```

## Design Philosophy

The goal is editable reconstruction, not pixel-perfect tracing. A good output should preserve the source page's structure, hierarchy, spacing, color intent, and meaning while avoiding SVG features that often break when converted into PowerPoint shapes.

For dense business slides, this skill favors clarity and editability over excessive decorative fidelity. Repeated icons and tiny visual markers should usually become simpler editable shapes.

## License

MIT License. See [LICENSE](LICENSE).
