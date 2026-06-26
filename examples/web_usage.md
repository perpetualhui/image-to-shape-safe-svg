# Web Usage

Prompt:

```text
Use $image-to-shape-safe-svg for a browser-based image-to-editable-SVG workflow.
Generate a web-safe pipeline that uploads PNG screenshots, reconstructs SVG, validates shape-safe constraints, and downloads svg_shape_safe.zip.
```

Key web constraints:

- Inline icon paths.
- Bake arrowheads.
- Do not use `<image>`, `<foreignObject>`, SVG markers, or transforms.
- Use `<tspan>` only inside `data-text-role="explanatory-block"` text when grouping same-style explanatory small text into one editable block.
- Validate before download.
