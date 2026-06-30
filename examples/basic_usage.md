# Basic Usage

Prompt:

```text
Use $image-to-shape-safe-svg to convert these three slide screenshots into editable SVG.
Only deliver individual SVG files. Make sure icons and arrowheads survive PowerPoint convert-to-shapes.
```

Required first response before conversion:

```text
Do you want me to preserve all source icons, or should I simplify decorative/repeated icons?
Choices: preserve_all, balanced, minimal.
```

For multi-page conversion, also ask:

```text
Do you want a validation/delivery report in addition to the SVG files?
```

Expected output by default:

```text
svg_shape_safe/
|-- 01_example.svg
|-- 02_example.svg
`-- 03_example.svg
```

Do not create `shape_safe_delivery_report.json` or a ZIP unless the user asks for it.

Every SVG should pass the hard metrics in `tools/validate_shape_safe_svg.py`.
