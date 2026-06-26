# Icon Matching

This skill includes a small built-in shape-safe icon library for business slides and diagrams.

The library is intentionally compact. It is not meant to reproduce every decorative source icon. It gives agents a predictable set of editable SVG primitives for common concepts such as workflow, automation, data, analytics, security, risk, cloud, users, teams, documents, checks, settings, and integrations.

## Files

```text
assets/icons/shape_safe_icon_library.json
assets/icons/semantic_icon_map.json
tools/match_shape_safe_icon.py
```

## Matching Rule

When an icon is useful, match source labels or section meaning against `semantic_icon_map.json`.

Examples:

```text
automation -> automation
数据平台 -> data or cloud, depending on page context
risk warning -> risk
compliance security -> security
workflow process -> workflow
```

If there is no good match, use the `workflow` fallback or replace the icon with a symbolic marker such as a numbered circle, small dot, status badge, or color chip.

Icon matching does not replace the mandatory user decision. Before final conversion, ask whether the user wants to preserve all source icons. If the user chooses `preserve_all`, match and rebuild every visible source icon that is reasonably reconstructable. If a match is uncertain, report it instead of silently simplifying.

## CLI Examples

Print only the matched icon name:

```bash
python tools/match_shape_safe_icon.py "automated approval workflow" --name-only
```

Render an absolute-coordinate SVG snippet:

```bash
python tools/match_shape_safe_icon.py "risk warning" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

Windows:

```powershell
py tools\match_shape_safe_icon.py "数据平台" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

The generated snippet does not use `<image>`, `transform`, `marker`, `foreignObject`, or `data-icon`.

## Reconstruction Guidance

- Use these icons only for primary modules, major conclusions, important risks, or high-level categories.
- Do not use a unique icon for every bullet unless the user chose `preserve_all`.
- For repeated items, prefer numbered circles, dots, pills, color chips, or badges only when the user chose `balanced` or `minimal`.
- After matching, paste or generate the expanded primitives into the final SVG. Do not leave a placeholder.
- If auto-matching returns a visually or semantically wrong icon, use a simpler marker or ask for confirmation instead of forcing the match.
