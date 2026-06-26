# Web Usage

Prompt:

```text
Use $image-to-shape-safe-svg for a browser-based image-to-editable-SVG workflow.
Generate a web-safe pipeline that uploads PNG screenshots, reconstructs SVG, validates shape-safe constraints, and downloads svg_shape_safe.zip.
```

The web UI must ask this before SVG generation:

```text
Do you want to preserve all source icons?
```

Supported choices:

- `preserve_all`
- `balanced`
- `minimal`

Key web constraints:

- Inline icon paths.
- Do not auto-simplify icons before the user chooses an icon-retention strategy.
- Bake arrowheads.
- Do not use `<image>`, `<foreignObject>`, SVG markers, or transforms.
- Use `<tspan>` only inside `data-text-role="explanatory-block"` text when grouping same-style explanatory small text into one editable block.
- Validate before download.
