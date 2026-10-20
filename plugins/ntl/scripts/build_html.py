#!/usr/bin/env python3
"""Build NTL HTML documents (handbook PDF, self-contained slides, quiz) anywhere, without the ntl-training-hub repo.

    python3 build_html.py init handbook|slides|quiz|course|topic|workshop <dir>   copy a template into <dir>
    python3 build_html.py pdf    <doc.html>    [--out DIR] [--name NTL-ALLME101-T01-Handbook]
    python3 build_html.py slides <slides.html> [--out DIR] [--name NTL-Workshop-Title-Slides]
    python3 build_html.py quiz   <quiz.html>   [--out DIR] [--name NTL-AIQAE101-L0-01-Quiz]

pdf     A4 PDF via Chrome headless. SVGs referenced by <img src="….svg"> are inlined so their text uses the page's
        DejaVu fonts. Table-of-contents numbers (<span class="pg" data-find="CHƯƠNG 3">) are found in the PDF and
        written back into the source, re-rendering until stable.
slides  One self-contained HTML (images, SVGs and DejaVu fonts embedded; fonts subset when fontTools is installed)
        plus a PDF with one 16:9 page per slide.
quiz    Copied unchanged under its versioned name (version from "version" in the quiz-data block).

Output names: <name>-vY.Z, version from the cover's <b>Phiên bản Y.Z</b> (or quiz-data). Without --name the base is
"NTL-" + the words of <title>. Output goes next to the source unless --out is given.
Requires Google Chrome/Chromium (set CHROME=/path if not found). Optional: poppler (pdftotext/pdfinfo) or pypdf
for TOC page numbers; fontTools for glyph checks and font subsetting.
"""
import argparse, base64, html as _h, io, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
ASSETS = PLUGIN / "assets"
TEMPLATES = PLUGIN / "skills" / "training" / "templates"
if not TEMPLATES.is_dir():   # standalone skill zip: <skill>/common/scripts/build_html.py, templates in <skill>/templates
    TEMPLATES = PLUGIN.parent / "templates"
PG = re.compile(r'(<span class="pg" data-find="([^"]+)">)([^<]*)(</span>)')
SVG_IMG = re.compile(r'<img\b([^>]*?)\bsrc="([^"]+\.svg)"([^>]*)>')
RASTER_IMG = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+\.(png|jpe?g|gif|webp))(")', re.I)
KINDS = {"handbook": "handbook.html", "slides": "slides.html", "quiz": "quiz.html",
         "course": "course.md", "topic": "topic.md", "workshop": "workshop.md"}


def find_chrome():
    cands = [os.environ.get("CHROME"),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium",
             r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser"),
             shutil.which("chrome")]
    for c in cands:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome/Chromium not found. Install Google Chrome or set CHROME=/path/to/chrome.")


def page_title(src):
    t = re.search(r"<title>([^<]*)</title>", src)
    return _h.unescape(t.group(1)).strip() if t else ""


def name_words(s):
    """"ChatGPT Work case study" -> "ChatGPT-Work-Case-Study": drop Vietnamese diacritics, capitalise each word, keep capitals."""
    import unicodedata
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "-".join(w[:1].upper() + w[1:] for w in re.findall(r"[A-Za-z0-9]+", s))


def versioned(base, src):
    v = re.search(r"<b>Phiên bản\s+(\d+(?:\.\d+)*)</b>", src) or re.search(r"<b>Version\s+(\d+(?:\.\d+)*)</b>", src)
    return f"{base}-v{v.group(1)}" if v else base


def base_name(src, given, kind):
    if given:
        return given
    words = name_words(page_title(src)) or "Document"
    return f"NTL-{words}" + ("-Slides" if kind == "slides" and not words.endswith("Slides") else "")


def inline_svgs(src, base):
    """<img class="dia" src="assets/fig-01.svg"> -> <svg class="dia" …> (file content, ids prefixed with "fig-01-")."""
    def rep(m):
        f = (base / m.group(2)).resolve()
        if not f.exists():
            sys.exit(f"Diagram not found: {m.group(2)} (from {base})")
        svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", f.read_text(encoding="utf-8")).strip()
        cls = re.search(r'\bclass="([^"]*)"', m.group(1) + m.group(3))
        if cls and not re.match(r'<svg\b[^>]*\bclass=', svg):
            svg = svg.replace("<svg", f'<svg class="{cls.group(1)}"', 1)
        ids = set(re.findall(r'\bid="([^"]+)"', svg))
        if ids:
            alt = "|".join(re.escape(i) for i in sorted(ids, key=len, reverse=True))
            svg = re.sub(rf'(\bid="|url\(#|href="#)({alt})(?=[")])', lambda g: f"{g.group(1)}{f.stem}-{g.group(2)}", svg)
        return svg
    return SVG_IMG.sub(rep, src)


def inline_images(src, base):
    """<img src="assets/shot-01.png"> -> data URI, so the slides travel as one file."""
    def rep(m):
        f = (base / m.group(2)).resolve()
        if not f.exists():
            sys.exit(f"Image not found: {m.group(2)} (from {base})")
        mime = "jpeg" if m.group(3).lower() == "jpg" else m.group(3).lower()
        return f"{m.group(1)}data:image/{mime};base64,{base64.b64encode(f.read_bytes()).decode()}{m.group(4)}"
    return RASTER_IMG.sub(rep, src)


def embed_fonts(src):
    """Insert the @font-face rules of assets/style.css (DejaVu, "Mono VN") with the fonts as data URIs.
    With fontTools only the glyphs the page uses are kept; without it the whole font is embedded."""
    text = _h.unescape(re.sub(r"<[^>]+>", "", src)) + "".join(map(chr, range(32, 127)))
    cache = {}

    def data(name):
        if name not in cache:
            path = ASSETS / "fonts" / name
            try:
                from fontTools import subset
                opts = subset.Options()
                opts.layout_features = ["*"]
                opts.drop_tables += ["FFTM"]
                font = subset.load_font(str(path), opts)
                sub = subset.Subsetter(opts)
                sub.populate(text=text)
                sub.subset(font)
                buf = io.BytesIO()
                font.save(buf)
                raw = buf.getvalue()
            except ImportError:
                raw = path.read_bytes()
            cache[name] = base64.b64encode(raw).decode()
        return cache[name]
    css = (ASSETS / "style.css").read_text(encoding="utf-8")
    faces = [re.sub(r'url\("fonts/([^"]+)"\)', lambda m: f"url(data:font/ttf;base64,{data(m.group(1))})", f)
             for f in re.findall(r"@font-face\{[^}]*\}", css)]
    return src.replace("</head>", f"<style>{''.join(faces)}</style>\n</head>", 1)


def check_glyphs(src):
    """Warn about characters DejaVu Sans lacks, and mono-block characters the "Mono VN" fallback does not cover."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("  (glyph check skipped: pip install fonttools)")
        return
    cmap = TTFont(ASSETS / "fonts" / "DejaVuSans.ttf").getBestCmap()
    text = _h.unescape(re.sub(r"<style.*?</style>|<[^>]+>", "", src, flags=re.S))
    missing = sorted({c for c in text if ord(c) > 127 and not c.isspace() and ord(c) not in cmap})
    if missing:
        print(f"  ⚠ characters missing from DejaVu Sans: {' '.join(missing)}")
    mono = TTFont(ASSETS / "fonts" / "DejaVuSansMono.ttf").getBestCmap()
    css = (ASSETS / "style.css").read_text(encoding="utf-8")
    ur = re.search(r'font-family:"Mono VN".*?unicode-range:([^}]+)\}', css, re.S)
    covered = set()
    for part in (ur.group(1).split(",") if ur else []):
        a, _, b = part.strip().replace("U+", "").partition("-")
        covered.update(range(int(a, 16), int(b or a, 16) + 1))
    blocks = re.findall(r'<pre class="(?:code|prompt)">(.*?)</pre>|<code>(.*?)</code>|<span class="kw">(.*?)</span>', src, re.S)
    mono_text = _h.unescape(re.sub(r"<[^>]+>", "", "".join(x for t in blocks for x in t)))
    bad = sorted({c for c in mono_text if ord(c) > 127 and ord(c) not in mono and ord(c) not in covered})
    if bad:
        print(f"  ⚠ mono-block characters without a fallback glyph (diacritics will break): {' '.join(bad)}")


def check_anchors(src):
    ids = set(re.findall(r'\bid="([^"]+)"', src))
    bad = sorted({h for h in re.findall(r'href="#([^"]+)"', src) if h not in ids})
    if bad:
        print(f"  ⚠ #anchor links without a target: {', '.join(bad)}")


def render(chrome, html, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--run-all-compositor-stage-before-draw", "--virtual-time-budget=5000",
                    f"--print-to-pdf={out}", Path(html).resolve().as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def page_texts(pdf):
    """Text of every page: poppler if installed, else pypdf, else None."""
    if shutil.which("pdftotext") and shutil.which("pdfinfo"):
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
        return [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout
                for i in range(1, n + 1)]
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]


def npages(pdf):
    t = page_texts(pdf)
    return len(t) if t is not None else "?"


def build_pdf(chrome, html, out):
    """doc.html -> out (PDF); fills the table-of-contents page numbers back into doc.html."""
    src = html.read_text(encoding="utf-8")
    full = inline_svgs(src, html.parent)
    check_glyphs(full)
    check_anchors(full)
    keys = [g.group(2) for g in PG.finditer(src)]
    page = html.with_name(f".{html.stem}.build.html")   # next to the source so relative paths (CSS, fonts, SVG) resolve
    try:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "t.pdf"
            for attempt in range(1, 5):
                page.write_text(inline_svgs(src, html.parent), encoding="utf-8")
                render(chrome, page, tmp)
                if not keys:
                    break
                texts = page_texts(tmp)
                if texts is None:
                    print("  ⚠ TOC page numbers not filled: install poppler (pdftotext) or `pip install pypdf`")
                    break
                found = {}
                for i, t in enumerate(texts, 1):
                    if i < 3:   # skip cover + table of contents
                        continue
                    for k in keys:
                        if k not in found and k in t:
                            found[k] = i
                missing = [k for k in keys if k not in found]
                if missing:
                    sys.exit(f"Not found in the PDF (data-find must match the rendered heading text): {missing}")
                new = PG.sub(lambda g: f"{g.group(1)}{found[g.group(2)]}{g.group(4)}", src)
                if new == src:
                    break
                html.write_text(new, encoding="utf-8")
                src = new
                print(f"  TOC page numbers updated (pass {attempt})")
            else:
                sys.exit("TOC page numbers did not converge")
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(tmp, out)
    finally:
        page.unlink(missing_ok=True)


def build_slides(chrome, html, outdir, name):
    """slides.html -> outdir/<name>.html (self-contained) + outdir/<name>.pdf (one 16:9 page per slide)."""
    src = html.read_text(encoding="utf-8")
    full = inline_images(inline_svgs(src, html.parent), html.parent)
    check_glyphs(full)
    check_anchors(full)
    full = embed_fonts(full)
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:   # render from a temp path: the target may contain spaces or diacritics
        page, pdf = Path(td) / "s.html", Path(td) / "s.pdf"
        page.write_text(full, encoding="utf-8")
        render(chrome, page, pdf)
        shutil.copyfile(page, outdir / f"{name}.html")
        shutil.copyfile(pdf, outdir / f"{name}.pdf")
    return [outdir / f"{name}.html", outdir / f"{name}.pdf"]


def init(kind, target, force=False):
    """Copy a template into target/ (index.html or <kind>.md) with the shared NTL assets as target/ntl-assets/."""
    target = Path(target).resolve()
    tpl = TEMPLATES / KINDS[kind]
    if tpl.suffix == ".md":
        dst = target / f"{kind}.md"
        if dst.exists() and not force:
            sys.exit(f"{dst} exists (use --force to overwrite)")
        target.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tpl, dst)
        print(f"✓ {dst}")
        return
    dst = target / "index.html"
    if dst.exists() and not force:
        sys.exit(f"{dst} exists (use --force to overwrite)")
    src = tpl.read_text(encoding="utf-8").replace('"../assets/', '"ntl-assets/')
    target.mkdir(parents=True, exist_ok=True)
    if '"assets/' in src:
        (target / "assets").mkdir(exist_ok=True)
    dst.write_text(src, encoding="utf-8")
    for f in (TEMPLATES / "assets").glob("*") if '"assets/' in src else ():
        if not (target / "assets" / f.name).exists():
            shutil.copyfile(f, target / "assets" / f.name)
    if "ntl-assets/" in src:
        na = target / "ntl-assets"
        (na / "fonts").mkdir(parents=True, exist_ok=True)
        for f in ("style.css", "cover-tri.svg"):
            shutil.copyfile(ASSETS / f, na / f)
        for f in (ASSETS / "fonts").iterdir():
            shutil.copyfile(f, na / "fonts" / f.name)
    print(f"✓ {dst}")


def main():
    ap = argparse.ArgumentParser(description="Build NTL HTML documents.", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("kind", choices=KINDS); p.add_argument("dir"); p.add_argument("--force", action="store_true")
    for c in ("pdf", "slides", "quiz"):
        p = sp.add_parser(c); p.add_argument("file"); p.add_argument("--out"); p.add_argument("--name")
    a = ap.parse_args()
    if a.cmd == "init":
        return init(a.kind, a.dir, a.force)
    html = Path(a.file).resolve()
    if not html.exists():
        sys.exit(f"File not found: {a.file}")
    src = html.read_text(encoding="utf-8")
    outdir = Path(a.out).resolve() if a.out else html.parent
    if a.cmd == "quiz":
        v = re.search(r'"version"\s*:\s*"([^"]+)"', src)
        out = outdir / f"{base_name(src, a.name, 'quiz')}{f'-v{v.group(1)}' if v else ''}.html"
        outdir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(html, out)
        print(f"✓ {out}")
        return
    chrome = find_chrome()
    name = versioned(base_name(src, a.name, a.cmd), src)
    if a.cmd == "pdf":
        out = outdir / f"{name}.pdf"
        build_pdf(chrome, html, out)
        print(f"✓ {out} ({npages(out)} pages)")
    else:
        for f in build_slides(chrome, html, outdir, name):
            print(f"✓ {f}" + (f" ({npages(f)} slides)" if f.suffix == ".pdf" else f" ({f.stat().st_size / 1e6:.1f} MB)"))


if __name__ == "__main__":
    main()
