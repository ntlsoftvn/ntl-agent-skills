#!/usr/bin/env python3
"""Maintainer tool: build upload files for apps that cannot add the marketplace from Git.

    python3 tools/pack.py [--out dist]

Writes
  dist/ntl.plugin             the plugin folder as a zip (.claude-plugin/plugin.json at its root), for Claude Cowork
  dist/ntl-<skill>.zip        one self-contained skill per zip, for ChatGPT Work (Skills > Upload):
                              a single folder ntl-<skill>/ with the skill plus the shared references/, assets/ and
                              scripts/ copied into ntl-<skill>/common/; links and the name are rewritten to match.
"""
import argparse, re, shutil, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "ntl-plugin"
SKIP = {".DS_Store", "__pycache__", "node_modules", ".index.build.html"}
SHARED = ("references", "assets", "scripts")


def files(base):
    for f in sorted(base.rglob("*")):
        if f.is_file() and not any(p in SKIP or p.endswith(".pyc") for p in f.relative_to(base).parts):
            yield f


def zip_dir(src, out, prefix=""):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files(src):
            z.write(f, f"{prefix}{f.relative_to(src).as_posix()}")


def rewrite_md(text, depth):
    """Point plugin-level paths at the bundled common/ folder. depth = folder depth below the skill root."""
    up = "../" * depth
    text = re.sub(r"(\.\./){%d}(references|assets|scripts)/" % (depth + 2), f"{up}common/\\2/", text)
    text = text.replace("`PLUGIN`: `SKILL_DIR/../..` (the plugin root)", "`PLUGIN`: `SKILL_DIR/common` (shared NTL files bundled with this skill)")
    return text


def pack_skill(skill_dir, out_dir):
    name = f"ntl-{skill_dir.name}"
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / name
        shutil.copytree(skill_dir, dst, ignore=shutil.ignore_patterns(*SKIP, "*.pyc"))
        for part in SHARED:
            shutil.copytree(PLUGIN / part, dst / "common" / part, ignore=shutil.ignore_patterns(*SKIP, "*.pyc"))
        for md in dst.rglob("*.md"):
            if (dst / "common") in md.parents:
                continue
            depth = len(md.relative_to(dst).parts) - 1
            md.write_text(rewrite_md(md.read_text(encoding="utf-8"), depth), encoding="utf-8")
        sk = dst / "SKILL.md"
        sk.write_text(re.sub(r"(?m)^name:\s*\S+", f"name: {name}", sk.read_text(encoding="utf-8"), count=1), encoding="utf-8")
        leftovers = [str(m.relative_to(dst)) for m in dst.rglob("*.md")
                     if (dst / "common") not in m.parents and re.search(r"\.\./\.\./(\.\./)?(references|assets|scripts)/", m.read_text(encoding="utf-8"))]
        if leftovers:
            sys.exit(f"plugin-relative links left in {leftovers}")
        out = out_dir / f"{name}.zip"
        zip_dir(Path(td), out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "dist"))
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    p = out / "ntl.plugin"
    zip_dir(PLUGIN, p)
    print(f"✓ {p} ({p.stat().st_size / 1e6:.1f} MB)")
    for sk in sorted(d for d in (PLUGIN / "skills").iterdir() if (d / "SKILL.md").exists()):
        z = pack_skill(sk, out)
        print(f"✓ {z} ({z.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
