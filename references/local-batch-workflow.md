# Local Batch Workflow

Use this workflow when Codex has filesystem access and can run Python/PowerShell.

## Folder Pattern

```text
batch-conversion-N/
|-- build_batch_svgs.py
|-- make_shape_safe_svgs.py
|-- data/
|-- reports/
`-- svg_shape_safe/
```

Only individual `.svg` files in `svg_shape_safe/` are user-facing output by default. Temporary `svg_output/` or `svg_final/` may exist during processing but should be deleted after delivery.

Do not create a ZIP unless the user explicitly asks for compressed packaging.

## Fast Path

1. Create a new batch folder. Do not overwrite earlier user-fixed batches.
2. Create a preflight note for each page: complexity level, estimated icon count, text density risk, visual-model call budget, icon-retention decision status, typography assumptions, and report preference.
3. For multi-page batches, pick one style anchor page first and use it as the reference for the rest of the batch.
4. Before writing final SVGs, always ask the user whether to preserve all source icons. Do not continue until the user chooses `preserve_all`, `balanced`, or `minimal`, unless the current request already specified one.
5. For multi-page batches, ask whether the user wants `shape_safe_delivery_report.json`. Do not generate the report by default.
6. Lock the typography scale for the whole batch: Microsoft YaHei plus `24 / 18 / 16 / 14 / 12 / 10 / 8`.
7. Write `build_batch_svgs.py` to reconstruct pages as structured SVG.
8. Use placeholders only internally if needed, such as `data-icon`, then expand them before delivery.
9. Run the shape-safe conversion step.
10. Bake all marker arrows into polygons.
11. Validate hard metrics.
12. Render PNG previews with Chrome or another SVG renderer.
13. Inspect previews and patch layout problems.

## Implementation Notes

- Use absolute canvas coordinates.
- Use one helper for structural single-line text nodes. Use this only for titles, KPI numbers, labels, badges, axis labels, process labels, and other standalone text:

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

- Use a separate helper for explanatory body paragraphs. Use this when several adjacent visual lines belong to one semantic paragraph, note, benefit statement, or supporting bullet group:

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

- One semantic paragraph must become one editable text box. Do not split body paragraphs into one text node per visual line.
- Do not use the explanatory block helper for titles, KPI numbers, labels, legends, badges, process labels, or text crossing card/column boundaries.
- Use only the fixed typography scale: `24 / 18 / 16 / 14 / 12 / 10 / 8`. Do not introduce arbitrary intermediate font sizes unless explicitly documented.
- Match icons from the bundled SVG icon library and expand them into paths/shapes.
- Keep only meaningful icons only after the user chooses `balanced` or `minimal`. Convert minor or repeated icons into numbered circles, dots, rounded pills, color chips, or badges only when that choice allows it.
- Record the required icon strategy as `preserve_all`, `balanced`, or `minimal` before writing final SVGs.
- For batches that should feel like one deck, keep palette, typography scale, icon treatment, card radius, and spacing consistent across pages; compare each new page against the anchor and the previous page.
- Convert all arrows into path/line plus polygon arrowheads.
- Re-render previews after every meaningful layout fix.

## Delivery Report

Ask before saving a multi-page JSON report. If the user approves a report, save these fields per file:

```json
{
  "file": "svg_shape_safe/example.svg",
  "complexity": "medium",
  "delivery": "individual_svg",
  "zip_requested": false,
  "report_requested": true,
  "icon_retention_decision": "balanced",
  "icon_strategy": "balanced",
  "font_family": "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
  "font_size_scale": [24, 18, 16, 14, 12, 10, 8],
  "paragraph_text_box_policy": "one_semantic_paragraph_per_text_box",
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
