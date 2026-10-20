# Diagrams (SVG, shared)

Architecture overviews, process flows and concept figures for any NTL document. Draw them as hand-written SVG; a generated layout (Graphviz etc.) usually ends up unreadable at slide size.

## Files

- One figure per file: `assets/fig-NN.svg`, where NN is the figure number ("Hình N" in Vietnamese documents). Numbering is continuous within a document; when inserting or removing a figure, rename the later files and update `src`, `alt`, captions and every mention.
- HTML documents reference them with `<img class="dia" src="assets/fig-03.svg" alt="Hình 3">`; the build inlines the SVG so its text uses the page's DejaVu font (opening the HTML directly shows the wrong font — judge figures in the build or the preview).
- For .pptx decks, convert to PNG at 1.5–2× (`rsvg-convert -z 1.5 fig.svg -o fig.png`, or `PLUGIN/scripts/preview_svg.py`) and place the PNG.

## Drawing conventions

- Root: `<svg viewBox="0 0 700 H" xmlns="http://www.w3.org/2000/svg">` for A4 (700 ≈ the text column); about 1000 wide for 16:9 slides. Choose H to fit the content snugly.
- Every `<text>` sets `font-family="DejaVu Sans, sans-serif"`. A4 sizes 8–12 (box labels 10–10.5, group titles 12, notes 8.5–9 in muted); on slides text ≥ 14. Multi-line text uses `<tspan x=… dy=…>` with a line step ≈ 1.3 × font size.
- Palette from `brand.md` only: navy `#14264A`/`#1F396D`/`#3B5690`, orange `#F16D22`, orange text `#C9520F`, light background `#F1F4FA`, border `#D5DBE7`, text `#1E2637`, muted `#667085`; tints `#DCE3F0`/`#E9EEF7`/`#FDE7D9` for bands. White text on navy or orange fills.
- Orange marks the one thing to notice (the key step, the new component, the risk zone). Everything else is navy or neutral.
- Boxes `rx="8"` (group containers `rx="10"`). Arrows: `<marker id="ah-<HEX>" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#<HEX>"/></marker>` in the file's own `<defs>`, stroke ≈ 1.6. Dashed lines for optional or legacy paths.
- Sizing text: DejaVu Sans is wide — estimate ≈ 0.6 × font size per character (≈ 0.65 bold) and keep ≥ 8 units of padding inside boxes; Vietnamese diacritics need ≥ 4 units vertically.
- Architecture diagrams: high level (one box per service or group), label every arrow with what flows ("pull jobs (TLS)"), put a one-line legend or note for anything not obvious (e.g. "provider not fixed yet").

## Check

`python3 PLUGIN/scripts/preview_svg.py assets/fig-03.svg [--out DIR] [--scale 2]` renders PNGs with the DejaVu fonts; read them and look for text overflowing or touching box edges, overlapping labels, arrows that miss their target, and centring. Then check the figure in the built document (not split across a page break, readable at the final size).
