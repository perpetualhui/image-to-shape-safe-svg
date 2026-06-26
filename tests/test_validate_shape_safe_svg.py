from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate_shape_safe_svg.py"


def run_validator(path: Path):
    return subprocess.run([sys.executable, str(TOOL), str(path), "--json"], capture_output=True, text=True)


def test_valid_svg_passes(tmp_path):
    svg = tmp_path / "valid.svg"
    svg.write_text('<svg><text x="1" y="2">OK</text><polygon data-baked-arrowhead="true" points="0,0 1,1 0,2"/></svg>', encoding="utf-8")
    result = run_validator(svg)
    assert result.returncode == 0


def test_forbidden_image_fails(tmp_path):
    svg = tmp_path / "bad.svg"
    svg.write_text('<svg><image href="x.png"/></svg>', encoding="utf-8")
    result = run_validator(svg)
    assert result.returncode == 1
