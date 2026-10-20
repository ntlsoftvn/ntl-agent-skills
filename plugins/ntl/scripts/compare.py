#!/usr/bin/env python3
"""Compare 2 PDFs: page count, embedded fonts, text differences, per-page pixel differences.

    python3 compare.py <new.pdf> <old.pdf>

<old.pdf> is the build from before the change (copy the PDF aside before editing the source) or the previous release.
Needs poppler (pdfinfo, pdftotext, pdffonts, pdftoppm); Pillow (pip install pillow) for the pixel comparison.
"""
import collections, re, subprocess, sys, tempfile
from pathlib import Path
if len(sys.argv) != 3:
    sys.exit(__doc__)
built, ref = Path(sys.argv[1]), Path(sys.argv[2])
run = lambda *a: subprocess.run(a, capture_output=True, text=True).stdout
pages = lambda p: int(re.search(r"Pages:\s+(\d+)", run("pdfinfo", str(p))).group(1))
words = lambda p: collections.Counter(run("pdftotext", str(p), "-").split())
fonts = lambda p: sorted({re.sub(r"^[A-Z]+\+", "", l.split()[0]) for l in run("pdffonts", str(p)).splitlines()[2:] if l.strip()})

print(f"pages : built={pages(built)}  ref={pages(ref)}")
print(f"font  : built={fonts(built)}\n        ref  ={fonts(ref)}")
a, b = words(built), words(ref)
print(f"words : only in built={sum((a-b).values())}, only in ref={sum((b-a).values())}  (expect ~0 when content is unchanged)")
print("        e.g. only in built:", list((a - b).items())[:12])
print("        e.g. only in ref  :", list((b - a).items())[:12])
try:
    from PIL import Image, ImageChops
    with tempfile.TemporaryDirectory() as td:
        run("pdftoppm", "-r", "40", "-png", str(built), f"{td}/b"); run("pdftoppm", "-r", "40", "-png", str(ref), f"{td}/r")
        bs, rs = sorted(Path(td).glob("b-*.png")), sorted(Path(td).glob("r-*.png"))
        res = []
        for i, (x, y) in enumerate(zip(bs, rs), 1):
            d = ImageChops.difference(Image.open(x).convert("L"), Image.open(y).convert("L"))
            res.append((i, round(sum(d.histogram()[40:]) / (d.size[0] * d.size[1]) * 100, 2)))
        print("pixels: % changed per page (>1% worth a look):", [(i, p) for i, p in res if p > 1] or "none")
except ImportError:
    print("pixels: skipped (pip install pillow)")
