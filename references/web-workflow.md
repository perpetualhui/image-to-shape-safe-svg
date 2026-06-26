# Web Workflow

Use this workflow when the task runs in a browser, web app, serverless function, or hosted agent where local filesystem paths and PowerShell are not reliable.

## Web-Safe Architecture

```text
Upload image(s)
  -> vision/structure extraction
  -> mandatory icon-retention choice
  -> normalized page JSON
  -> SVG reconstruction
  -> icon expansion
  -> arrowhead baking
  -> validation
  -> browser preview
  -> download svg_shape_safe.zip
```

## Required Web Output

Return final SVG files only. Do not expose intermediate `svg_output`.

Before SVG generation or download, the UI must ask whether to preserve all source icons. Continue only after the user chooses:

- `preserve_all`: rebuild every visible source icon that can reasonably become editable SVG.
- `balanced`: keep meaningful section/module icons and simplify decorative or repeated icons.
- `minimal`: remove most decorative icons and use typography, spacing, color, and simple markers.

For batch output, download:

```text
svg_shape_safe.zip
├── page_01.svg
├── page_02.svg
├── page_03.svg
└── shape_safe_delivery_report.json
```

## Browser Rendering Rules

- Use SVG DOM APIs or a server-side XML builder, not string patches over arbitrary uploaded SVG.
- Inline icon paths from a bundled icon set at generation time.
- Do not simplify, remove, or replace source icons until the user has made the required icon-retention choice.
- Do not use external icon URLs; they may fail offline or disappear during Office conversion.
- Avoid CSS-dependent layout for important geometry. Prefer explicit attributes on each element.
- Avoid `foreignObject`; Office conversion is unreliable.
- Avoid `textPath` and transformed text.
- Avoid `tspan` except inside approved explanatory small-text blocks marked with `data-text-role="explanatory-block"`.

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
- Dense Chinese explanatory text is grouped into editable multi-line text blocks when the lines share the same style and paragraph meaning.
- Final SVG contains no embedded raster image.

## Recommended JSON Shape Schema

Use a normalized page JSON before SVG generation:

```json
{
  "canvas": {"width": 2400, "height": 1350},
  "icon_retention_decision": "balanced",
  "texts": [{"x": 92, "y": 112, "lines": ["Title"], "size": 54, "weight": 850}],
  "shapes": [{"type": "rect", "x": 100, "y": 200, "w": 300, "h": 80, "fill": "#fff"}],
  "icons": [{"name": "chart-bar", "cx": 200, "cy": 300, "size": 56}],
  "arrows": [{"points": [[100, 100], [200, 100]], "stroke": "#5A0FB4", "width": 4}],
  "groups": [{"id": "side-panel", "children": []}]
}
```

This makes web workflows easier to debug and lets a human reviewer fix structure before SVG generation.
