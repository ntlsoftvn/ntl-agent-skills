# Slides (HTML deck → self-contained HTML + 16:9 PDF)

For talks: a workshop or a topic that is presented. (Proposal decks for customers are a different skill: `proposal`, .pptx.)

Create: `python3 <PLUGIN>/scripts/build_html.py init slides <dir>` → `<dir>/index.html` with every layout as a sample, `<dir>/assets/`.
Build: `python3 <PLUGIN>/scripts/build_html.py slides <dir>/index.html --out <dist> --name <base>`:

- workshop: `--name NTL-Workshop-<Title-Words>-Slides` (words of the title without diacritics, first letters capitalised, existing capitals kept: "ChatGPT Work case study" → `NTL-Workshop-ChatGPT-Work-Case-Study-Slides`);
- topic of a course: `--name NTL-<COURSE>-<TOPIC>-Slides`.

Output `<base>-vY.Z.html` (images, SVGs and DejaVu fonts embedded: can be sent or presented offline) and `<base>-vY.Z.pdf` (one page per slide). Y.Z comes from the cover's `<b>Phiên bản Y.Z</b>` line, which must stay.

## Rules

- Set `<title>` (the workshop name), `--footer-text` and the cover. Keep the template's style and script unchanged inside a deck.
- One `<section class="slide">` per slide, **one idea per slide**, at most ~6 bullets. Body text 24px, never below 17px.
- What the presenter says goes in `<aside class="notes">` (shown with `N`, never printed).
- Layouts in the template: `cover` · plain (h2 + `.rule` + content) · `section` · `.cols2/.cols3` + `.card` (`.card.o` = emphasis) · `figure` with `img.dia` (SVG) or `figure.shot` (screenshot; `div.ph` as placeholder) · `.steps` (numbered process, `div.hl` = emphasis) · `table` (+ `td.k`, `.c`) · `blockquote.quote`, `.big` · `ul.check` · `pre.prompt` (text typed to an AI; wrap `@app`/`@skill` in `span.at`) · `.note` / `.callout` · `end`. Copy the layouts you need and delete the other samples.
- Images in `assets/`: screenshots `shot-NN.png`, diagrams `fig-NN.svg` drawn per `diagrams.md` for 16:9 (viewBox about 1000 wide, text ≥ 14). Never put a literal `<img …>` tag inside an HTML comment (the build would try to inline it).
- Keys when presenting: ← → / Space / PageUp PageDown, Home End, `N` notes, `F` full screen, `#5` in the URL opens slide 5.

## Check

Render the PDF (`pdftoppm -r 40 -png …`) and look at every slide: nothing cut off or overflowing, no near-empty slide. Open the built HTML and step through with ←/→ and `N`. For a workshop, the minutes in `workshop.md` add up to the slot.
