# PowerPoint decks (.pptx, shared)

NTL decks are generated with pptxgenjs through `PLUGIN/scripts/ntl_deck.js`, so every deck gets the same cover, title rule, footer, page numbers and components (`brand.md`). Write a build script per deck (start from an example such as `skills/proposal/examples/proposal_deck.js`), keep the content in one block at the top, and rebuild after every change. Never hand-edit the generated .pptx.

## Setup (once per machine)

1. `node --version` (Node 18+). If missing, ask the user to install Node.js from https://nodejs.org; don't continue without it.
2. Tell the user it will download the npm packages pptxgenjs, react, react-dom, react-icons and sharp, then run
   `sh PLUGIN/scripts/setup_node.sh`. It installs into `~/.cache/ntl-agent-skills/node` (or a temp folder when the home folder is not writable; `NTL_NODE_CACHE=<dir>` to choose) and prints the folder to use as `NODE_PATH`. Re-running it is cheap.
3. Build: `NODE_PATH=<printed path> node <work>/build_deck.js <out.pptx> [diagram_dir]`. Set `NTL_PLUGIN=<PLUGIN>` when the build script is not inside the plugin.

## Library (`ntl_deck.js`)

```js
const ntl = require(path.join(PLUGIN, "scripts", "ntl_deck.js"));
const d = ntl.createDeck({ project, docType: "Proposal", version: "2.0", date: "10/2026", total: 11 });
d.cover({ title, subtitle });                    // navy cover, white NTL logo, triangles, kicker, version line (logo: false to omit)
d.agenda([["Summary", 3], ...]);                   // numbered agenda with page numbers
const s = d.content("Section", "Slide title");     // title + orange rule + footer + "N / total"
d.txt(s, text, opts)  d.card(s, x, y, w, h, name, topColor)  d.box(s, x, y, w, h, "note"|"callout", name, text)
d.lead("Label: ", "rest")  d.bullets([...])  d.numbered(s, [[title, text], ...], opts)  d.image(s, file, opts)
d.table(s, header, rows, opts)  d.stats(s, [[value, label], ...])  d.gantt(s, { weeks, block, phases })
d.barChart(s, { labels, values, title })  await d.iconCircle(s, ReactIcon, x, y, dia)  await d.save(out)
```

- Geometry: `d.X0`, `d.XW`, `d.Y0` give the content box (inches); `d.px()` converts template pixels; `d.pt()` converts template pixel font sizes to points. Colours: `ntl.H` (hex from `brand.md`).
- `d.save` warns when `total` differs from the number of slides; fix the agenda page numbers at the same time.
- `d.image` draws a labelled placeholder when the file is missing, so a deck builds before its diagrams exist.
- pptxgenjs rules that bite: hex colours without `#`; one option object per call (pptxgenjs mutates them); `bullet: true`-style lists via `d.bullets`, never a literal "•"; native charts only (`addChart`).

## QA loop (after every build)

1. If the Anthropic pptx skill's `validate.py` is available, run it; otherwise make sure the file opens.
2. `sh PLUGIN/scripts/render.sh <deck.pptx> <out_dir> [dpi]` (Keynote on macOS, else LibreOffice; PNG via poppler). Look at every slide image: text overflowing a box, a title or subtitle wrapping onto a second line for one word, overlapping shapes, near-empty slides, footer and page numbers right.
3. Keynote does not draw pptxgenjs charts: check chart slides in PowerPoint or LibreOffice, or say you could not.
4. If no renderer is installed, say that visual QA was skipped.

## Diagrams in decks

Draw SVG per `diagrams.md` (viewBox about 1000 wide for a slide), convert to PNG at 1.5× (`rsvg-convert -z 1.5`, or render with `preview_svg.py --scale 1.5`) and place it with `d.image`.
