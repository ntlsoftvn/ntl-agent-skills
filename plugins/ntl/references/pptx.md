# PowerPoint decks (.pptx, shared)

NTL decks are generated with python-pptx through `PLUGIN/scripts/ntl_deck.py`, so every deck gets the same cover, title rule, footer, page numbers and components (`brand.md`). The cover and content layouts (title placeholder, orange rule, footer) live in the file's slide layouts `NTL_COVER` / `NTL_CONTENT`, so a user can still add slides or edit the footer in PowerPoint. Write a build script per deck (start from an example such as `skills/proposal/examples/proposal_deck.py`), keep the content in one block at the top, and rebuild after every change. Never hand-edit the generated .pptx.

## Setup (once per machine)

1. `python3 --version` (Python 3.9+; the command is `python` on Windows, and wherever `python3` is not found; below, `python3` means whichever one exists). If missing, ask the user to install Python from https://www.python.org/downloads/; don't continue without it.
2. If `python3 -c "import pptx"` fails, tell the user it will download the pip package python-pptx, then run
   `sh PLUGIN/scripts/setup_python.sh`. It installs into `~/.cache/ntl-agent-skills/python` (or a temp folder when the home folder is not writable; `NTL_PY_CACHE=<dir>` to choose); `ntl_deck.py` finds that folder on its own. Re-running it is cheap.
3. Build: `python3 <work>/build_deck.py <out.pptx> [diagram_dir]`. Set `NTL_PLUGIN=<PLUGIN>` when the build script is not inside the plugin.

## Library (`ntl_deck.py`)

```python
import sys; sys.path.insert(0, f"{PLUGIN}/scripts")
import ntl_deck as ntl
d = ntl.create_deck(project=..., doc_type="Proposal", version="2.0", date="10/2026", total=11)
d.cover(title=..., subtitle=...)                   # navy cover, white NTL logo, triangles, kicker, version line (logo=False to omit)
d.agenda([("Summary", 3), ...])                    # numbered agenda with page numbers
s = d.content("Section", "Slide title")            # title + orange rule + footer + "N / total"
d.txt(s, text, x=, y=, w=, h=, size=, bold=, color=, align=, valign=, space_after=)
d.card(s, x, y, w, h, name, top)   d.box(s, x, y, w, h, "note"|"callout", name, text)
d.lead("Label: ", "rest")   d.bullets([...])   d.numbered(s, [(title, text), ...])   d.image(s, file, x=, y=, w=, h=)
d.table(s, header, rows, col_w=[...])   d.stats(s, [(value, label), ...])   d.gantt(s, weeks=, block=, phases=)
d.bar_chart(s, labels=, values=, title=)   d.icon_circle(s, png, x, y, dia)   d.save(out)
d.rect / d.rounded / d.oval / d.hline / d.line   # primitives, all with name= for the object name
```

- Text content is a str, or a list of paragraphs; a paragraph is a str, a run dict `{"text": .., "bold": True, "color": ..}` or a list of those (runs in one paragraph). `d.lead()` and `d.bullets()` return ready-made paragraph lists.
- Geometry: `d.X0`, `d.XW`, `d.Y0` give the content box (inches); `d.px()` converts template pixels; `d.pt()` converts template pixel font sizes to points. Colours: `ntl.H` (dict of hex values from `brand.md`, no `#`).
- `d.save` warns when `total` differs from the number of slides; fix the agenda page numbers at the same time.
- `d.image` draws a labelled placeholder when the file is missing, so a deck builds before its diagrams exist.
- Icons: `d.icon_circle` takes a PNG with a transparent background (white glyph). Render one from an SVG with `preview_svg.py` or `rsvg-convert`; there is no icon font bundled.
- Native charts only (`bar_chart`); no screenshots of charts.

## QA loop (after every build)

1. If the Anthropic pptx skill's `validate.py` is available, run it; otherwise make sure the file opens.
2. `sh PLUGIN/scripts/render.sh <deck.pptx> <out_dir> [dpi]` (Keynote on macOS, else LibreOffice; PNG via poppler). Look at every slide image: text overflowing a box, a title or subtitle wrapping onto a second line for one word, overlapping shapes, near-empty slides, footer and page numbers right.
3. Keynote may not draw native charts: check chart slides in PowerPoint or LibreOffice, or say you could not.
4. If no renderer is installed, say that visual QA was skipped.

## Diagrams in decks

Draw SVG per `diagrams.md` (viewBox about 1000 wide for a slide), convert to PNG at 1.5× (`rsvg-convert -z 1.5`, or render with `preview_svg.py --scale 1.5`) and place it with `d.image`.
