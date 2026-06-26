from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHECKS = {
    "image": re.compile(r"<image\b", re.I),
    "data_icon": re.compile(r"data-icon=", re.I),
    "transform": re.compile(r"\btransform=", re.I),
    "marker_end": re.compile(r"\bmarker-end=", re.I),
    "marker_defs": re.compile(r"<marker\b", re.I),
    "foreign_object": re.compile(r"<foreignObject\b", re.I),
}
TSPAN = re.compile(r"<tspan\b", re.I)
EXPLANATORY_TEXT_BLOCK = re.compile(
    r"<text\b(?=[^>]*\bdata-text-role\s*=\s*['\"]explanatory-block['\"])[\s\S]*?</text>",
    re.I,
)
CHECK_ORDER = [*CHECKS, "tspan"]


def validate_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    result: dict[str, object] = {"file": str(path)}
    for name, pattern in CHECKS.items():
        result[name] = len(pattern.findall(text))
    total_tspan = len(TSPAN.findall(text))
    allowed_tspan = sum(
        len(TSPAN.findall(match.group(0))) for match in EXPLANATORY_TEXT_BLOCK.finditer(text)
    )
    result["tspan"] = max(0, total_tspan - allowed_tspan)
    result["explanatory_tspan"] = allowed_tspan
    result["shape_safe_icons"] = text.count('data-shape-safe-icon="true"')
    result["baked_arrowheads"] = text.count('data-baked-arrowhead="true"')
    result["ok"] = all(result[name] == 0 for name in CHECK_ORDER)
    return result


def iter_svg_paths(target: Path) -> list[Path]:
    if target.is_file() and target.suffix.lower() == ".svg":
        return [target]
    return sorted(target.rglob("*.svg"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Office shape-safe SVG constraints.")
    parser.add_argument("target", help="SVG file or directory containing SVG files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        raise SystemExit(f"Target does not exist: {target}")

    results = [validate_file(path) for path in iter_svg_paths(target)]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            status = "OK" if item["ok"] else "FAIL"
            print(f"{status} {item['file']}")
            for name in CHECK_ORDER:
                print(f"  {name}: {item[name]}")
            print(f"  explanatory_tspan: {item['explanatory_tspan']}")
            print(f"  shape_safe_icons: {item['shape_safe_icons']}")
            print(f"  baked_arrowheads: {item['baked_arrowheads']}")
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
