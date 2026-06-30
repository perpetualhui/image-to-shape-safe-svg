---
name: image-to-shape-safe-svg
description: Convert slide-like images, screenshots, flowcharts, business diagrams, or infographic PNG/JPG pages into Office/PPT shape-safe editable SVG. Use when the user wants image-to-SVG reconstruction, editable icons/arrows/text, batch conversion, web-compatible SVG output, or SVGs that survive PowerPoint "convert to shapes" without losing icons, arrows, or text layout.
metadata:
  short-description: Image to editable shape-safe SVG
---

# Image To Shape-Safe SVG

Use this skill to reconstruct slide-like raster images into editable, Office-safe SVGs. The goal is not bitmap tracing. The goal is a structured SVG made from text, paths, lines, polygons, icons, and simple shapes that can later be edited or converted to shapes without losing content.

Default aesthetic bias: reduce decorative icons. Use icons only when they clarify the content hierarchy. For secondary or repetitive items, prefer numbered circles, small dots, rounded pills, color chips, status badges, or simple button-like shapes with a restrained palette.

Mandatory icon-retention gate: before any SVG reconstruction, batch conversion, or final shape-safe conversion, ask the user whether they want to preserve all source icons. This is required even when the page looks simple. Do not proceed to final conversion until the user answers, unless the current user message already gives an explicit icon strategy.

Default autonomy rule: when a conversion would materially change the source design, especially by reducing many icons, merging crowded pages, or splitting/reflowing content, pause before final shape conversion and give the user a small set of choices.

## Output Contract

Deliver final outputs as individual standalone `.svg` files by default.

Do not output `.zip` archives unless the user explicitly requests compressed packaging. If a folder structure is useful, use a folder named `svg_shape_safe`, but still deliver individual SVG files whenever the runtime supports direct SVG file output.

For multi-page conversion, ask whether the user wants a validation/delivery report before generating `shape_safe_delivery_report.json`. Do not include the report by default unless the user requests it, the workflow requires it, or the user has already approved report generation.

Hard validation targets for every delivered SVG:

- `image = 0`
- `data_icon = 0`
- `transform = 0`
- `marker_end = 0`
- `marker_defs = 0`
- `tspan = 0`, except approved explanatory small-text blocks marked with `data-text-role="explanatory-block"`
- `foreign_object = 0`

Practical meaning:

- Do not embed the source image or full-page screenshots.
- Expand icon placeholders into real SVG paths before delivery.
- Bake arrowheads as polygons, not SVG markers.
- Use independent single-line `<text x y>...</text>` nodes for titles, numbers, labels, badges, axis labels, process labels, and short standalone callouts.
- Use one editable text box per semantic paragraph for body/explanatory text. When a paragraph spans multiple visual lines, use one `<text data-text-role="explanatory-block">` with child `<tspan>` lines.
- Avoid transforms; place each shape with absolute coordinates.

In validation reports, `tspan` means disallowed tspan count. Approved explanatory paragraph lines inside `<text data-text-role="explanatory-block">` are reported separately as `explanatory_tspan`. Do not use `tspan` for headings, numbers, icons, labels, badges, legends, or unrelated text groups.

### File Delivery Policy

Default delivery:

- Output a single standalone `.svg` file for each converted page.
- Do not output `.zip` archives by default.
- Do not bundle SVGs unless the user explicitly asks for batch packaging.
- For single-page conversion, return one standalone SVG file.
- For multi-page conversion, return multiple individual SVG files if supported.
- Ask before creating a multi-page validation/delivery report.

If direct SVG file attachment is not supported:

- Provide the SVG source code directly or use the least compressed/non-archive delivery option available.
- Do not create a ZIP merely to work around SVG attachment limitations unless the user approves.

### Default Delivery, Typography, And Text-Box Policy

Unless the user specifies otherwise, apply these defaults across the whole output, not slide by slide:

- Delivery: individual standalone SVG files; no ZIP unless explicitly requested.
- Report: ask before producing a multi-page validation/delivery report.
- Font: `Microsoft YaHei, Noto Sans SC, Arial, sans-serif`.
- Font-size scale: `24 / 18 / 16 / 14 / 12 / 10 / 8`.
- Text grouping: one semantic paragraph per editable text box.
- Body paragraphs: use `data-text-role="explanatory-block"` with `<tspan>` lines when multiple visual lines belong to one paragraph.
- Shape safety: no embedded images, no `foreignObject`, no transforms, no SVG markers, no icon placeholders.
- PowerPoint conversion priority: editable structure and clean text boxes take priority over pixel-perfect tracing.

## When To Use Which Reference

- For local desktop/batch work, read `references/local-batch-workflow.md`.
- For browser/web-app workflows, read `references/web-workflow.md`.
- For semantic icon matching, read `docs/icon-matching.md` and use `tools/match_shape_safe_icon.py`.
- For layout/icon/arrow pitfalls, read `docs/troubleshooting.md`.
- For maps, geography, coverage diagrams, or dense polygon assets, read `docs/map-complexity-policy.md` before reconstruction.
- For automated checks, use `tools/validate_shape_safe_svg.py`.

## Recommended Workflow

1. Inspect the source image dimensions and composition.
2. Create a short preflight plan: complexity level, estimated icon count, text density, risky regions, layout strategy, visual-model call budget, required icon-retention question, typography assumptions, and report preference when the job has multiple pages.
3. Ask the mandatory icon-retention question before conversion: "Do you want to preserve all source icons, or should I simplify decorative/repeated icons?" Offer exactly these choices unless the user already specified one:
   - Preserve all: keep every visible source icon that can reasonably be rebuilt as editable SVG.
   - Balanced: keep meaningful section/module icons and convert minor repeated icons to badges, dots, or numbered markers.
   - Minimal: remove most decorative icons and rely on typography, spacing, color, and simple markers.
4. Rebuild the page structurally: title, subtitle, sections, cards, flows, arrows, side panels, footer.
5. If the page contains a map or dense geographic outline, treat it as a complex polygon asset: place a simple editable placeholder first, finish the rest of the page, and handle the map last.
6. Decide whether each icon is necessary. Keep only icons that represent primary modules, major conclusions, or high-level categories; replace decorative or repetitive icons with dots, numbered circles, pills, color chips, or badges.
7. Draw arrows as lines or paths plus baked polygon arrowheads.
8. Place headings, labels, badges, numbers, and short standalone callouts as independent text nodes. Place each body paragraph or explanatory paragraph in one editable text box.
9. Generate intermediate SVGs only if needed, then produce individual final SVG files.
10. Validate hard metrics.
11. Render previews and visually inspect for text overlap, missing necessary icons, over-iconized pages, missing arrowheads, map overflow, and layout drift.

## Reconstruction Rules

- Prefer simple primitives: `rect`, `circle`, `line`, `path`, `polygon`, `text`.
- Use explicit coordinates; avoid `g transform`, `scale`, `translate`, and nested transformed groups.
- Prefer visual fidelity for structure, spacing, color, and hierarchy over pixel-perfect tracing.
- Keep text shorter or split lines when needed. Text stability after Office conversion is more important than matching exact source line breaks.
- For headings, KPI numbers, labels, short chips, and independent bullets, use one text node per visual line.
- For body/explanatory text, one semantic paragraph must become one editable text box. Do not split one paragraph into one text box per visual line.
- For explanatory small text, merge adjacent same-style lines into one editable multi-line text block. This is required for 12, 14, and 16 px body/explanation text when the lines are a paragraph, note, bullet group, or supporting description.
- Use a small, deliberate icon budget. A typical business slide should have about 3-5 meaningful icons, not one icon for every bullet. Dense module overview pages may use more, but repeated icons should be simplified into badges or markers.
- Match icons from the bundled semantic icon library first (`assets/icons/shape_safe_icon_library.json`). Use `tools/match_shape_safe_icon.py` to expand a semantic label into absolute SVG primitives. Do not embed icon images or leave icon placeholders in final SVG.
- Prefer symbolic shape replacements for minor items: numbered circles for steps, small filled circles for bullet groups, rounded pills for statuses, color chips for categories, and compact badges for "standardized", "automated", "traceable", or similar labels.
- Use color semantically. Keep a primary brand color, one accent color, and neutral grays unless the source page already uses a richer but meaningful palette.
- Treat tiny connector arrows as high-risk. Draw them explicitly and validate them in preview.
- Treat maps, coastlines, country borders, and dense coverage regions as high-risk complex polygons. Default to an abstract network/coverage placeholder unless the map is the main subject.
- Do not spend the first reconstruction pass tracing a world map. Build the editable slide structure first, then decide whether the map needs a simplified outline, an abstract replacement, or a separately sourced simplified asset.

## Typography System

For Chinese business-slide reconstruction, use this typography system across the entire page or batch unless the user or client specifies otherwise.

Default font:

- `Microsoft YaHei`
- Fallback: `Microsoft YaHei, Noto Sans SC, Arial, sans-serif`

Allowed font-size scale:

- `24 px`
- `18 px`
- `16 px`
- `14 px`
- `12 px`
- `10 px`
- `8 px`

Default mapping:

- Page title: `24 px`, bold.
- Subtitle or small text below title: `18 px`.
- Section/module title: `18 px`, bold.
- Card title: `18 px`, bold.
- Main body text: `16 px`.
- Dense body text: `14 px`.
- Secondary notes, captions, legends: `12 px`.
- Fine print or compact annotations: `10 px` or `8 px`.

Do not use arbitrary intermediate sizes such as `17`, `19`, `21`, or `23` unless the user explicitly requests them or visual reconstruction absolutely requires a documented exception.

When text is crowded:

- Prefer adjusting line breaks, card spacing, and text box width before changing the typography system.
- Prefer reducing body text from `16 px` to `14 px` before distorting layout.
- Use `12 px`, `10 px`, or `8 px` only for clearly secondary information.
- Do not mix unrelated font scales across pages in one batch. Lock the scale from the style anchor and reuse it.

## Text Box Grouping Policy

One semantic paragraph must become one editable text box.

Do:

- Main title: one text box.
- Subtitle or module title: one text box.
- Phase label with two lines: one text box if both lines name the same phase.
- Card title: one text box.
- Card body paragraph: one text box.
- Benefit or conclusion sentence: one text box.
- Numbered circle value: independent text.
- Process labels such as `P2P`, `O2C`, `R2R`: independent text.

Do not:

- Split one paragraph into one text box per visual line.
- Merge unrelated paragraphs across cards, columns, grid cells, or semantic sections.
- Merge text with different semantic roles merely because it is close together.
- Use paragraph `<tspan>` grouping for headings, numbers, badges, standalone labels, legends, or icons.

## Text Grouping For Explanatory Small Text

Explanatory small text means supporting copy that is visually subordinate to a title, KPI, step label, card heading, or section heading. It often appears as two or more short lines with similar size, weight, color, and line spacing.

Default behavior:

- Merge explanatory lines into one logical text box when they share the same font size, weight, fill, alignment, and semantic paragraph.
- Prefer body sizes 16, 14, and 12. If the source uses smaller text, reduce only as needed, but keep each merged block internally consistent.
- Keep line height about `1.25-1.45 * font-size`, with a little extra space for dense Chinese.
- Use separate text boxes when font size, weight, color, indentation, or semantic role changes.
- Do not merge across card boundaries, column boundaries, dividers, flow steps, or unrelated bullet groups.
- Keep each explanatory block to a readable size. If a block would become a dense paragraph that is hard to select or align, split it by semantic paragraph rather than by every visual line.

SVG pattern:

```xml
<text x="640" y="420" font-family="Microsoft YaHei, Noto Sans SC, Arial, sans-serif" font-size="14" fill="#333" data-text-role="explanatory-block">
  <tspan x="640" dy="0">第一行解释文字</tspan>
  <tspan x="640" dy="19">第二行解释文字</tspan>
  <tspan x="640" dy="19">第三行解释文字</tspan>
</text>
```

Use this exception only for explanatory small text. Do not use `tspan` for icons, headings, KPI numbers, legends that need separate positioning, or text that should remain independently selectable.

## Pre-Generation Typography And Layout Confirmation

Before final SVG generation, briefly confirm typography and layout assumptions when:

- The source image has dense text.
- The source uses inconsistent font sizes.
- The client may require a specific font or font-size hierarchy.
- The conversion target is PowerPoint shape conversion.
- The reconstruction requires meaningful reflow, resizing, or simplification.
- The job has multiple pages and may need a validation/delivery report.

Ask concise questions such as:

- Should I use the default Microsoft YaHei typography scale: `24 / 18 / 16 / 14 / 12 / 10 / 8`?
- Should body text prioritize readability after PowerPoint shape conversion, even if the layout differs slightly from the source image?
- Should each semantic paragraph be grouped into one editable text box?
- For multi-page conversion, do you want a validation/delivery report?
- Are there any client-specific font, color, spacing, or title-size requirements?

If the user has already provided a standing preference, apply it without repeatedly asking.

## Preflight Complexity And Vision Budget

Before reconstructing, classify the image. This prevents over-spending effort on low-value details and makes high-risk conversions explicit.

- Simple: title, few blocks, low text density, no dense icons or map. Use one visual read plus one rendered preview inspection.
- Medium: several cards, flow arrows, charts, or moderate Chinese text. Use one visual read, one layout reconstruction pass, and one preview comparison.
- Complex: dense infographic, many icons, several nested panels, small text, dashboard-style layout, map/network, or multiple flow branches. Use an initial visual read, a focused second read for risky regions, and a final preview comparison.
- Very complex: tiny text everywhere, heavy screenshots, dense maps, complicated tables, or icon count so high that editability conflicts with fidelity. Ask the user whether to prioritize fidelity, editability, or executive simplification before final conversion.

Suggested visual-model call budget when a vision model is available:

- Simple: 1 source analysis call.
- Medium: 1 source analysis call plus 1 preview/layout check if needed.
- Complex: 2 source/risky-region calls plus 1 preview/layout check.
- Very complex: ask before using more than 3 calls or before doing a major restyle.

The preflight summary should be short and actionable. Include:

- Complexity level.
- Estimated meaningful icon count and decorative icon count.
- Mandatory icon-retention decision status: `preserve_all`, `balanced`, `minimal`, or `not_answered`.
- Text density risk.
- Layout strategy.
- Whether user choice is needed before reducing icons, splitting pages, or applying a merge/restyle strategy.

## Icon Economy

Before drawing icons, classify each visual marker:

- Primary icon: keep it if it names a major section, module, capability, risk, or conclusion.
- Repeated category marker: usually convert it into a numbered circle, color chip, or simple badge.
- Bullet decoration: remove it or replace it with a small dot.
- Tiny icon inside dense text: remove it unless the source relies on it for meaning.

Avoid generating many icons just because the original image contains many small visual decorations. Too many editable icons make the PPT harder to read, slower to edit, and more fragile after PowerPoint conversion.

Always ask before converting to final shapes whether all source icons should be preserved. Offer no more than three clear choices:

- Preserve all: keep every visible source icon that can reasonably be rebuilt as editable SVG.
- Balanced: keep only section/module icons and convert minor icons to badges or markers.
- Minimal: remove most decorative icons and use typography, spacing, and color blocks instead.

Do not silently choose `balanced` or `minimal`. If the user has not answered the icon-retention question, stop before final conversion and ask.

Good substitutions:

- Step cards: numbered circles instead of unique icons.
- Status lists: rounded pills or check badges instead of repeated icons.
- Category legends: color chips and short labels instead of icon sets.
- Dense financial or operational notes: text hierarchy, dividers, and spacing instead of icons.

## Built-In Icon Matching

Use the bundled icon library before inventing new icons:

```bash
python tools/match_shape_safe_icon.py "automation workflow" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

The tool matches semantic labels in English, Chinese, and Japanese against `assets/icons/semantic_icon_map.json`, then emits expanded SVG primitives from `assets/icons/shape_safe_icon_library.json`.

Rules:

- Use matched icons for primary sections, modules, risks, capabilities, and conclusions.
- If the match is weak, use a symbolic marker instead of forcing an unrelated icon.
- If the user chose `preserve_all`, replace each source icon with the closest editable shape-safe equivalent and report any icon that could not be matched confidently.
- Paste or generate the expanded primitive output into final SVGs.
- Never leave `data-icon`, nested icon placeholders, or embedded icon images in delivered SVGs.

## High-Frequency Failure Rules

Recent repeated issues should be handled as hard checks:

- User was not asked about icon preservation: stop and ask before final conversion.
- Too many icons made the SVG noisy or fragile: ask again before simplifying; do not assume simplification is allowed.
- Auto-matched icon looks semantically wrong: replace with a simpler badge/marker or report the uncertainty instead of forcing the match.
- Icon placeholders remained in output: expand them into primitives before delivery; `data_icon` must be 0.
- Icons survived validation but visually crowded text or arrows: reduce size, move them, or ask whether simplification is acceptable.
- Different pages in a batch use inconsistent icon styles: lock an icon style from the anchor page and reuse it.

## Layout Judgment For PPT Merge Or Restyle

When a request involves merging, restyling, or converting multiple pages into a PPT-like deck, do not blindly preserve every original layout. Prefer a user-facing choice when the conversion would meaningfully change structure:

- Preserve original: keep the source layout, only fix fonts, alignment, validation issues, and shape safety.
- Light unification: keep each page's structure but unify title style, margins, colors, icon style, and footer/header treatment.
- Recommended optimization: preserve the main message while reducing decorative icons, improving spacing, simplifying dense regions, and replacing minor icons with badges or markers.
- Executive simplification: split or compress crowded pages so each slide has one main point, key numbers, and only essential visuals.
- Template adaptation: fit content into a provided master/template and discard source layouts that conflict with the template grid.

Keep layouts that have clear hierarchy, readable text, stable grids, meaningful color, and one dominant message. Discard or rewrite layouts that are crowded, over-iconized, full of nested cards, mixed icon styles, arbitrary colors, or tiny text that will not survive PPT editing.

Lessons borrowed from presentation-generation workflows:

- Start with a plan, not shapes: decide slide purpose, hierarchy, style rules, and risk areas before drawing.
- Maintain style consistency across a batch: color palette, typography scale, icon treatment, card radius, and spacing should be stable.
- Do not batch style-critical reconstruction blindly. For pages that should belong to one deck, use the previous finished page as a style reference for the next page.
- Be specific about design rules: exact palette, font scale, spacing, and visual substitutions produce more consistent results than vague "make it professional" instructions.
- Limit each slide to one dominant message when restyling is allowed.

## Deck Consistency For Batches

When multiple pages should feel like one deck or one shared system:

- Define a style anchor page first. Use it to lock the palette, font scale, icon treatment, card radius, and spacing for the batch.
- Reuse the immediately previous finished page as the reference for the next page instead of re-deciding style from scratch.
- Keep each page to one dominant message and one focal hierarchy. If a page has multiple competing points, split or simplify before conversion.
- If a later page drifts away from the established system, pause and realign rather than forcing the whole batch forward.
- For style-critical pages, avoid blind bulk reconstruction; do the batch sequentially and compare each page against the anchor and the previous page.

## Naming

Use readable English slugs:

```text
01_non_merchandise_smart_operations_closed_loop.svg
12_ai_expense_implementation_roadmap.svg
13_intelligent_expense_management_platform.svg
```

For revised versions, append `_v2`, `_v3`, etc. rather than overwriting user-fixed files.

## Batch Size Guidance

For high-quality manual reconstruction:

- 3 pages per batch is comfortable for dense business diagrams.
- 4 pages per batch is acceptable when layouts are similar.
- 5+ pages should be split unless the user prioritizes speed over review quality.

## Verification

Run:

```bash
python tools/validate_shape_safe_svg.py path/to/svg_shape_safe
```

Then render previews with a browser or SVG renderer. A green validator report is necessary but not sufficient; always inspect the preview.
