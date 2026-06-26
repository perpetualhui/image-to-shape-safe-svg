# Local Batch Workflow

Use this workflow when Codex has filesystem access and can run Python/PowerShell.

## Folder Pattern

```text
batch-conversion-N/
├── build_batch_svgs.py
├── make_shape_safe_svgs.py
├── data/
├── reports/
└── svg_shape_safe/
```

Only `svg_shape_safe/` is user-facing output. Temporary `svg_output/` or `svg_final/` may exist during processing but should be deleted after delivery.

## Fast Path

1. Create a new batch folder. Do not overwrite earlier user-fixed batches.
2. Create a preflight note for each page: complexity level, estimated icon count, text density risk, visual-model call budget, and whether user choice is needed.
3. For multi-page batches, pick one style anchor page first and use it as the reference for the rest of the batch.
4. If a page is over-iconized or a major restyle/split is needed, ask the user before final shape conversion.
5. Write `build_batch_svgs.py` to reconstruct pages as structured SVG.
6. Use placeholders only internally if needed, such as `data-icon`, then expand them before delivery.
7. Run the shape-safe conversion step.
8. Bake all marker arrows into polygons.
9. Validate hard metrics.
10. Render PNG previews with Chrome or another SVG renderer.
11. Inspect previews and patch layout problems.

## Implementation Notes

- Use absolute canvas coordinates.
- Use one helper for structural single-line text nodes:

```python
def text(
    x,
    y,
    content,
    size=24,
    weight=400,
    fill="#111",
    anchor="start",
    font_family="Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
):
    parts = []
    for idx, line in enumerate(str(content).split("\n")):
        yy = y + idx * round(size * 1.34, 1)
        parts.append(f'<text x="{x}" y="{yy}" font-family="{font_family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(line)}</text>')
    return "\n".join(parts)
```

- Use a separate helper for explanatory small text blocks. Use this when several adjacent lines are the same 16, 14, or 12 px style and belong to one paragraph, note, or supporting bullet group:

```python
def explanatory_text_block(
    x,
    y,
    lines,
    size=14,
    weight=400,
    fill="#333",
    anchor="start",
    line_height=1.34,
    font_family="Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
):
    clean_lines = [line for line in [str(item).strip() for item in lines] if line]
    if not clean_lines:
        return ""
    dy = round(size * line_height, 1)
    attrs = (
        f'x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'font-family="{font_family}" fill="{fill}" text-anchor="{anchor}" '
        f'data-text-role="explanatory-block"'
    )
    parts = [f"<text {attrs}>"]
    for idx, line in enumerate(clean_lines):
        parts.append(f'<tspan x="{x}" dy="{0 if idx == 0 else dy}">{escape(line)}</tspan>')
    parts.append("</text>")
    return "\n".join(parts)
```

- Do not use the explanatory block helper for titles, KPI numbers, labels, legends that need independent positioning, or text crossing card/column boundaries.
- Match icons from a real SVG icon library and expand them into paths.
- Keep only meaningful icons by default. Convert minor or repeated icons into numbered circles, dots, rounded pills, color chips, or badges.
- For icon-heavy pages, record the proposed icon strategy as `preserve`, `balanced`, or `minimal` before writing final SVGs.
- For batches that should feel like one deck, keep palette, typography scale, icon treatment, card radius, and spacing consistent across pages; compare each new page against the anchor and the previous page.
- Convert all arrows into path/line plus polygon arrowheads.
- Re-render previews after every meaningful layout fix.

## Delivery Report

Save a JSON report with these fields per file:

```json
{
  "file": "svg_shape_safe/example.svg",
  "complexity": "medium",
  "icon_strategy": "balanced",
  "visual_model_calls_budget": 1,
  "image": 0,
  "data_icon": 0,
  "transform": 0,
  "marker_end": 0,
  "marker_defs": 0,
  "tspan": 0,
  "explanatory_tspan": 6,
  "foreign_object": 0,
  "shape_safe_icons": 18,
  "baked_arrowheads": 7
}
```
