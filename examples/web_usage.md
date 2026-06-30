# Web Usage

Prompt:

```text
Use $image-to-shape-safe-svg for a browser-based image-to-editable-SVG workflow.
Generate a web-safe pipeline that uploads PNG screenshots, reconstructs SVG, validates shape-safe constraints, and downloads individual SVG files.
```

The web UI must ask this before SVG generation:

```text
Do you want to preserve all source icons?
```

Supported choices:

- `preserve_all`
- `balanced`
- `minimal`

For multi-page conversion, the web UI must also ask:

```text
Do you want a validation/delivery report in addition to the SVG files?
```

Key web constraints:

- Inline icon paths.
- Do not auto-simplify icons before the user chooses an icon-retention strategy.
- Do not output ZIP archives unless the user explicitly requests compressed packaging.
- Ask before generating a multi-page validation/delivery report.
- Use Microsoft YaHei and the fixed `24 / 18 / 16 / 14 / 12 / 10 / 8` font-size scale across the whole output.
- Use one semantic paragraph per editable text box.
- Bake arrowheads.
- Do not use `<image>`, `<foreignObject>`, SVG markers, or transforms.
- Use `<tspan>` only inside `data-text-role="explanatory-block"` text when grouping same-style explanatory paragraph lines into one editable block.
- Validate before download.
