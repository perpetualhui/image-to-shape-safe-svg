from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
LIBRARY_PATH = ICON_DIR / "shape_safe_icon_library.json"
MAP_PATH = ICON_DIR / "semantic_icon_map.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pick_icon(query: str, library: dict, mapping: dict) -> str:
    text = query.casefold()
    aliases = mapping.get("aliases", {})
    matches = []
    for alias, icon_name in aliases.items():
        if alias.casefold() in text and icon_name in library["icons"]:
            matches.append((len(alias), alias, icon_name))
    if matches:
        matches.sort(reverse=True)
        return matches[0][2]

    best_name = mapping.get("default_icon", "workflow")
    best_score = 0
    for name, spec in library["icons"].items():
        score = 0
        if name.casefold() in text:
            score += 3
        for tag in spec.get("tags", []):
            if str(tag).casefold() in text:
                score += 2
        if score > best_score:
            best_name = name
            best_score = score
    return best_name


def scale(value: float, origin: float, size: float) -> float:
    return round(origin + (float(value) / 24.0) * size, 3)


def scaled_points(points: list, x: float, y: float, size: float) -> str:
    pairs = []
    for px, py in points:
        pairs.append(f"{scale(px, x, size)},{scale(py, y, size)}")
    return " ".join(pairs)


def render_icon(icon_name: str, library: dict, x: float, y: float, size: float, color: str) -> str:
    icon = library["icons"][icon_name]
    stroke_width = round((float(library.get("stroke_width", 1.8)) / 24.0) * size, 3)
    common = (
        f'stroke="{escape(color)}" stroke-width="{stroke_width}" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round" '
        'data-shape-safe-icon="true"'
    )
    parts = [f'<!-- shape-safe-icon: {escape(icon_name)} -->']
    for element in icon.get("elements", []):
        kind = element["type"]
        if kind == "line":
            parts.append(
                f'<line x1="{scale(element["x1"], x, size)}" y1="{scale(element["y1"], y, size)}" '
                f'x2="{scale(element["x2"], x, size)}" y2="{scale(element["y2"], y, size)}" {common}/>'
            )
        elif kind == "rect":
            rx = scale(element.get("rx", 0), 0, size)
            parts.append(
                f'<rect x="{scale(element["x"], x, size)}" y="{scale(element["y"], y, size)}" '
                f'width="{scale(element["width"], 0, size)}" height="{scale(element["height"], 0, size)}" '
                f'rx="{rx}" {common}/>'
            )
        elif kind == "circle":
            parts.append(
                f'<circle cx="{scale(element["cx"], x, size)}" cy="{scale(element["cy"], y, size)}" '
                f'r="{scale(element["r"], 0, size)}" {common}/>'
            )
        elif kind == "ellipse":
            parts.append(
                f'<ellipse cx="{scale(element["cx"], x, size)}" cy="{scale(element["cy"], y, size)}" '
                f'rx="{scale(element["rx"], 0, size)}" ry="{scale(element["ry"], 0, size)}" {common}/>'
            )
        elif kind == "polyline":
            parts.append(f'<polyline points="{scaled_points(element["points"], x, y, size)}" {common}/>')
        elif kind == "polygon":
            parts.append(f'<polygon points="{scaled_points(element["points"], x, y, size)}" {common}/>')
        elif kind == "path_polyline":
            points = element["points"]
            if not points:
                continue
            commands = [f'M {scale(points[0][0], x, size)} {scale(points[0][1], y, size)}']
            for px, py in points[1:]:
                commands.append(f'L {scale(px, x, size)} {scale(py, y, size)}')
            parts.append(f'<path d="{" ".join(commands)}" {common}/>')
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Match a semantic label to a shape-safe SVG icon snippet.")
    parser.add_argument("query", help="Semantic label or short phrase, such as automation, risk, workflow, or 数据")
    parser.add_argument("--x", type=float, default=0, help="Top-left x coordinate")
    parser.add_argument("--y", type=float, default=0, help="Top-left y coordinate")
    parser.add_argument("--size", type=float, default=48, help="Icon box size")
    parser.add_argument("--color", default="#333333", help="Stroke color")
    parser.add_argument("--name-only", action="store_true", help="Only print the matched icon name")
    args = parser.parse_args()

    library = load_json(LIBRARY_PATH)
    mapping = load_json(MAP_PATH)
    icon_name = pick_icon(args.query, library, mapping)
    if args.name_only:
        print(icon_name)
    else:
        print(render_icon(icon_name, library, args.x, args.y, args.size, args.color))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
