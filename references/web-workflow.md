# Web Workflow

Use this workflow when the task runs in a browser, web app, serverless function, or hosted agent where local filesystem paths and PowerShell are not reliable.

## Web-Safe Architecture

```text
Upload image(s)
  -> vision/structure extraction
  -> mandatory icon-retention choice
  -> optional report choice for multi-page jobs
  -> normalized page JSON
  -> SVG reconstruction
  -> icon expansion
  -> arrowhead baking
  -> validation
  -> browser preview
  -> download individual SVG file(s)
```

## Required Web Output

Return final SVG files only. Do not expose intermediate `svg_output`.

Before SVG generation or download, the UI must ask whether to preserve all source icons. Continue only after the user chooses:

- `preserve_all`: rebuild every visible source icon that can reasonably become editable SVG.
- `balanced`: keep meaningful section/module icons and simplify decorative or repeated icons.
- `minimal`: remove most decorative icons and use typography, spacing, color, and simple markers.

Before multi-page delivery, ask whether the user wants a validation/delivery report. Do not generate `shape_safe_delivery_report.json` by default.

For batch output, return individual SVG files by default:

```text
svg_shape_safe/
|-- page_01.svg
|-- page_02.svg
`-- page_03.svg
```

Only create `svg_shape_safe.zip` when the user explicitly requests compressed packaging.

## Browser Rendering Rules

- Use SVG DOM APIs or a server-side XML builder, not string patches over arbitrary uploaded SVG.
- Inline icon paths from a bundled icon set at generation time.
- Do not simplify, remove, or replace source icons until the user has made the required icon-retention choice.
- Do not use external icon URLs; they may fail offline or disappear during Office conversion.
- Avoid CSS-dependent layout for important geometry. Prefer explicit attributes on each element.
- Avoid `foreignObject`; Office conversion is unreliable.
- Avoid `textPath` and transformed text.
- Use the fixed typography scale across the whole page or batch: `24 / 18 / 16 / 14 / 12 / 10 / 8`.
- Use one semantic paragraph per editable text box.
- Avoid `tspan` except inside approved explanatory paragraph text blocks marked with `data-text-role="explanatory-block"`.

## Web Validation

Before enabling download, run the hard metric check:

```js
const forbidden = [
  /<image\b/i,
  /data-icon=/i,
  /\btransform=/i,
  /\bmarker-end=/i,
  /<marker\b/i,
  /<foreignObject\b/i
];
```

Count `<tspan>` separately. Allow it only when it is inside a `<text data-text-role="explanatory-block">...</text>` block; otherwise block or warn.

## Web UI Review Checklist

Show per-page preview thumbnails and flags:

- No missing icons.
- No missing arrowheads.
- No text overlap.
- Text remains inside boxes.
- Dense Chinese explanatory text is grouped into editable multi-line text boxes when the lines belong to the same semantic paragraph.
- Font sizes come from the fixed scale only.
- Final SVG contains no embedded raster image.

## Recommended JSON Shape Schema

Use a normalized page JSON before SVG generation:

```json
{
  "canvas": {"width": 2400, "height": 1350},
  "delivery": {"format": "individual_svg", "zip_requested": false, "report_requested": false},
  "icon_retention_decision": "balanced",
  "typography": {"font_family": "Microsoft YaHei, Noto Sans SC, Arial, sans-serif", "scale": [24, 18, 16, 14, 12, 10, 8]},
  "texts": [{"x": 92, "y": 112, "lines": ["Title"], "size": 24, "weight": 700, "role": "page_title"}],
  "paragraphs": [{"x": 160, "y": 260, "lines": ["Body line one", "Body line two"], "size": 16, "role": "explanatory-block"}],
  "shapes": [{"type": "rect", "x": 100, "y": 200, "w": 300, "h": 80, "fill": "#fff"}],
  "icons": [{"name": "chart-bar", "cx": 200, "cy": 300, "size": 56}],
  "arrows": [{"points": [[100, 100], [200, 100]], "stroke": "#5A0FB4", "width": 4}],
  "groups": [{"id": "side-panel", "children": []}]
}
```

This makes web workflows easier to debug and lets a human reviewer fix structure before SVG generation.
