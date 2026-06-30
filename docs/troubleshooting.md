# Troubleshooting

## User Was Not Asked About Icon Preservation

Cause: the conversion skipped the mandatory icon-retention gate.

Fix:

- Stop before final conversion.
- Ask: "Do you want to preserve all source icons, or should decorative/repeated icons be simplified?"
- Continue only after the user chooses `preserve_all`, `balanced`, or `minimal`, unless the current request already specified the strategy.
- Record the answer in the preflight note and delivery report.

## ZIP Was Produced Without Approval

Cause: the workflow treated batch delivery as a packaging problem and defaulted to `svg_shape_safe.zip`.

Fix:

- Deliver individual `.svg` files by default.
- Create ZIP archives only when the user explicitly asks for compressed packaging.
- If direct SVG attachment is unavailable, provide SVG source code or ask for approval before packaging.

## Multi-Page Report Was Produced Without Approval

Cause: the workflow generated `shape_safe_delivery_report.json` by default.

Fix:

- Ask before creating a multi-page validation/delivery report.
- Record `report_requested: true` only after user approval.
- Do not use report generation as a substitute for inspecting SVG previews.

## Icons Disappear After PowerPoint Conversion

Cause: icons were `<use>`, external SVG references, font icons, or raster images.

Fix:

- Expand icons into real `path`, `circle`, `rect`, etc.
- Add `data-shape-safe-icon="true"` for auditing.
- Validate `data_icon = 0` and `image = 0`.

## Arrowheads Disappear

Cause: SVG markers are not reliably preserved when converted to Office shapes.

Fix:

- Do not deliver `marker-end`.
- Draw the arrow shaft as a path/line.
- Draw the arrowhead as a small polygon with `data-baked-arrowhead="true"`.

## Text Becomes Scrambled Or Moves

Cause: unstructured multiline `tspan`, transformed text, tight boxes, or overly long lines.

Fix:

- Use independent `<text x y>` for titles, KPI numbers, labels, and individually positioned text.
- For same-style explanatory small text, group adjacent lines into one `data-text-role="explanatory-block"` text block.
- One semantic paragraph must be one editable text box; do not split one paragraph into one text node per visual line.
- Use only the fixed typography scale: `24 / 18 / 16 / 14 / 12 / 10 / 8`.
- Avoid `transform`.
- Split long Chinese sentences manually.
- Leave extra line height and box padding.

## Map Work Makes The Whole Slide Worse

Cause: maps, coastlines, country borders, and coverage regions are complex polygon assets. Trying to trace them early can consume the reconstruction budget and leave the real slide content less polished.

Fix:

- Read `docs/map-complexity-policy.md`.
- Place an editable placeholder first.
- Build titles, KPI blocks, cards, icons, labels, dividers, and legends before handling the map.
- Prefer abstract networks, region labels, or simplified landmass silhouettes unless the map is the main subject.
- Use Chrome/Playwright previews to verify the final effect, not only hard validation counts.

## The SVG Looks Less Pixel-Perfect Than The Image

This is expected. Pixel-perfect bitmap tracing often produces uneditable paths and fragile text. For Office-safe output, prioritize:

1. Editability
2. Stable text
3. Icons preserved as shapes
4. Arrows preserved as shapes
5. Visual similarity

## Batch Quality Drops

Reduce batch size. Dense business diagrams are safest at 3-4 pages per batch.

## Icon Matching Looks Wrong

Cause: semantic auto-matching chose a technically valid but visually misleading icon.

Fix:

- Prefer a neutral badge, numbered circle, dot, or color chip when confidence is low.
- If the user chose `preserve_all`, report unmatched or uncertain icons rather than silently dropping them.
- Keep icon style consistent across the batch by reusing the style anchor page.
