# Map Complexity Policy

Use this policy whenever a slide-like source contains world maps, country outlines, regional coverage maps, route maps, coastlines, borders, or any dense multi-polygon geographic asset.

The core rule:

> Treat maps as complex polygon assets, not as ordinary icons. Build the slide first, put a simple editable placeholder where the map belongs, and process the map last.

## Why This Exists

Maps can quickly dominate reconstruction complexity. Dense coastlines, country borders, and auto-traced shapes create many points and paths, which makes the SVG harder to edit in PowerPoint and can distract from higher-value work such as text hierarchy, icons, alignment, and business logic.

For business slides, the final communication effect is usually more important than geographic precision. If the map is only expressing "global coverage", "regional presence", or "network reach", use a cleaner editable abstraction instead of a detailed map.

## Role Classification

Classify the map before drawing it:

- Decorative background: the map only signals global/regional scope. Prefer an abstract globe, latitude/longitude ellipses, light coverage field, or node network.
- Information carrier: the map has dots, labels, routes, or regional coverage. Rebuild the dots, labels, routes, and callouts first; keep the base map faint or abstract.
- Main subject: the slide is fundamentally about geography, territories, facilities, routes, or markets. Use a dedicated map workflow and validate it separately.

Default to the lowest complexity that communicates the intent.

## Complexity Levels

Level A: Abstract coverage or network

- Use editable ellipses, grids, latitude/longitude lines, nodes, connector lines, and region labels.
- Best default for shape-safe PPT SVG.
- Use when the source map is only a visual metaphor for global reach.

Level B: Simplified outline

- Draw a rough outline for simple geography such as one country, Australia, a continent block, or a few regional blobs.
- Keep point count low.
- Do not draw country borders unless they carry information.

Level C: Low-fidelity world map

- Draw 5 to 7 simplified landmass silhouettes.
- Avoid detailed coastlines and internal borders.
- Use only as a faint background layer behind the real business content.

Level D: Precise or semi-precise map

- Use only when the map is the main subject or the user explicitly asks for geographic fidelity.
- Source a reliable simplified vector or TopoJSON asset, preferably from GitHub, Natural Earth, or another known open data source.
- Simplify geometry before embedding it.
- Validate the map in isolation, then combine it with the slide.

## Reconstruction Order

1. Inspect the source and classify the map role.
2. Place an editable placeholder in the map area: rectangle, ellipse, pale globe grid, or labeled coverage zone.
3. Build all low-risk elements first: title, subtitle, KPI blocks, cards, icons, captions, dividers, callouts, footer, and legends.
4. Render with Chrome and inspect the layout without the final map.
5. Decide whether the placeholder is enough. If yes, keep the abstract version.
6. If a map is still needed, implement only the minimum necessary complexity level.
7. Render again, inspect for text overlap and overflow, then run hard validation.

## Shape-Safe Rules For Maps

- No embedded map screenshots.
- No auto-traced dense coastline by default.
- No hundreds of small polygons unless the map is the slide's main subject and the user accepts lower editability.
- No `transform`, `marker`, `foreignObject`, or `<image>`.
- Do not use `tspan` inside map geometry, routes, labels that need independent placement, or legends. Use the skill's explanatory small-text block exception only for same-style notes outside the map object.
- Prefer absolute coordinates and simple primitives.
- Keep the map visually subordinate unless geography is the message.
- Put map labels, markers, routes, and legends in separate editable text/shape objects.

## Tool Preference

Use tools in this order when available:

1. Chrome for first visual rendering and screenshot checks.
2. Playwright for repeatable viewport screenshots and basic regression checks.
3. Computer User when PowerPoint import, ungrouping, or "convert to shapes" behavior must be verified.
4. GitHub or trusted open data sources for map assets when Level D is required.
5. Vercel or another web preview target when the user needs a shareable visual review.

## Red Flags

If any of these happen, stop refining the map and downgrade complexity:

- The map takes more effort than the business content.
- Text, icons, or cards start drifting because of map work.
- The SVG becomes hard to inspect or edit.
- The map is the largest or most complex object in a slide where geography is not the main message.
- The preview looks visually busy even though validation passes.

## Acceptance Standard

A map treatment is successful when:

- The slide communicates the intended coverage or geography clearly.
- The main business content remains editable and visually dominant.
- The SVG passes the hard validation checks.
- Chrome/Playwright preview shows no cropping, overlap, or layout drift.
- PowerPoint editability is preserved as much as possible for the actual user-facing elements.
