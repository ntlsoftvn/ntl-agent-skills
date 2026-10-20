# HTML documents → PDF (shared)

Handbooks, HTML slide decks and quizzes are written as HTML and built with `PLUGIN/scripts/build_html.py`. The HTML is the source; built files are derived and are never edited by hand.

```bash
python3 PLUGIN/scripts/build_html.py init handbook|slides|quiz|course|topic|workshop <dir>
python3 PLUGIN/scripts/build_html.py pdf    <dir>/index.html --out <dist> --name NTL-<COURSE>-<TOPIC>-Handbook
python3 PLUGIN/scripts/build_html.py slides <dir>/index.html --out <dist> --name NTL-Workshop-<Title>-Slides
python3 PLUGIN/scripts/build_html.py quiz   <dir>/index.html --out <dist> --name NTL-<COURSE>-<TOPIC>-Quiz
```

- `init` copies a template into `<dir>` together with `ntl-assets/` (the shared `style.css`, cover art and DejaVu fonts) so the document opens and builds on any machine. Don't edit `ntl-assets/`; refresh it with `init … --force` into a scratch folder if the plugin's style changes.
- `pdf`: renders with Chrome headless, inlines SVG figures (so their text uses DejaVu), and fills the table-of-contents page numbers (`<span class="pg" data-find="…">`) back into the source, re-rendering until stable. It stops if a `data-find` key is not found in the PDF.
- `slides`: one self-contained HTML (images, SVGs, fonts embedded; fonts subset when fontTools is installed) plus a PDF with one 16:9 page per slide.
- `quiz`: copies the file unchanged under its versioned name.
- Names: `<name>-vY.Z`, Y.Z from the cover's `<b>Phiên bản Y.Z</b>` (or `<b>Version Y.Z</b>`; quizzes: `"version"`). Without `--name` the base is `NTL-` + the words of `<title>`. Output goes next to the source unless `--out` is given.

## Requirements

| Tool | Needed for | If missing |
|---|---|---|
| Python 3.9+ | everything | — |
| Google Chrome or Chromium (`CHROME=/path` to point at it) | rendering | the build stops; ask the user to install Chrome |
| poppler (`pdftotext`, `pdfinfo`, `pdftoppm`) or `pip install pypdf` | TOC page numbers; `pdftoppm` for page previews | TOC numbers are left as they are, with a warning |
| `pip install fonttools` | glyph checks, smaller slide files | checks skipped, fonts embedded whole |
| `pip install pillow` + poppler | `compare.py` pixel diff | pixel part skipped |

## Checks after every build

1. Read every `⚠` line: characters missing from DejaVu, Vietnamese characters in code blocks without the "Mono VN" fallback, `#anchor` links with no target. Fix them or say why they stay.
2. Render the PDF to PNG (`pdftoppm -r 60 -png <pdf> <prefix>`; slides `-r 40`) and look at every page.
3. For a new version, `python3 PLUGIN/scripts/compare.py <new.pdf> <old.pdf>` (copy the old PDF aside before editing): differences must be exactly where you edited.
