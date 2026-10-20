#!/usr/bin/env python3
"""Render SVG diagrams to PNG with the NTL DejaVu fonts, to check for overflowing text or overlapping shapes
without building the whole document.

    python3 preview_svg.py assets/fig-02.svg [more.svg ...] [--out DIR] [--scale 2]

PNGs go to a fresh temp dir by default and their paths are printed; open them to check.
Render width = viewBox width x scale (handbook diagrams use a 700-wide viewBox, about the A4 text column).
"""
import argparse, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_html import ASSETS, find_chrome  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svgs", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--scale", type=float, default=2)
    a = ap.parse_args()
    chrome, out = find_chrome(), Path(a.out or tempfile.mkdtemp(prefix="ntl-svg-"))
    out.mkdir(parents=True, exist_ok=True)
    css = (ASSETS / "style.css").read_text(encoding="utf-8").replace('url("fonts/', f'url("{(ASSETS / "fonts").as_uri()}/')
    for s in a.svgs:
        f = Path(s).resolve()
        svg = f.read_text(encoding="utf-8")
        vb = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', svg)
        if not vb:
            sys.exit(f"{s}: missing viewBox")
        w, h = (round(float(x) * a.scale) for x in vb.groups())
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "p.html"
            page.write_text(f'<!doctype html><meta charset="utf-8"><style>{css}</style>'
                            f'<style>html,body{{margin:0;background:#fff}}svg{{display:block;width:{w}px;height:{h}px}}</style>{svg}',
                            encoding="utf-8")
            png = out / f"{f.stem}.png"
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                            "--allow-file-access-from-files", "--virtual-time-budget=3000", f"--screenshot={png}", page.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(png)


if __name__ == "__main__":
    main()
