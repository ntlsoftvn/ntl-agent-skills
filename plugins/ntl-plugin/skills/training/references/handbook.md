# Handbook (HTML source → A4 PDF)

The handbook HTML is the **single source of truth**; the PDF is derived and never edited by hand. Readers consume the A4 PDF, so every layout decision is judged on the PDF, not in a browser.

Create: `python3 <PLUGIN>/scripts/build_html.py init handbook <dir>` → `<dir>/index.html`, `<dir>/assets/fig-01.svg` (sample), `<dir>/ntl-assets/` (style.css, fonts; do not edit).
Build: `python3 <PLUGIN>/scripts/build_html.py pdf <dir>/index.html --out <dist> --name NTL-<COURSE>-<TOPIC>-Handbook` → `NTL-<COURSE>-<TOPIC>-Handbook-vY.Z.pdf` (Y.Z from `<b>Phiên bản Y.Z</b>` on the cover).

## Structure

Cover → Mục lục → Giới thiệu → Chương 1..N (one `<div class="page">` per chapter) → Phụ lục (checklists, Học thêm) → Glossary last.

- Set the topic in `<title>`, `--footer-text` (`<Course name>  ·  Topic <code>  ·  <Topic name>`) and the cover. The cover's `.layers` block is optional: keep it when the course has layers and mark the focus with class `on`; delete it otherwise.
- Each chapter opens with `<span class="chnum">Chương N</span><h1 class="ch">…</h1><div class="chrule"></div>`.
- Table of contents: `<span class="pg" data-find="CHƯƠNG N">`. `data-find` must equal the **rendered text** at the top of the chapter page (`.chnum` is uppercased by CSS). The build fills the numbers and stops when a key is not found.
- Chapters stay short (about 2–3 pages for an overview topic); keep frames, terms, decisions and pointers; move detail to an appendix or a later topic.

## Components (classes from style.css; examples in the template)

| Class | Use |
|---|---|
| `.lead` | 2–3 line chapter lead |
| `.note` | blue box: tip, summary |
| `.callout` | orange box: principle, pitfall |
| `.card`, `.card.o`, `.cols2`, `.cols3` | cards in a grid; `.o` = emphasis |
| `table` + `td.k` | tables; `td.k` = key column |
| `figure.fig` + `figcaption` | figure, caption "Hình N." + one sentence saying what to see |
| `.badge b0/b1/b2` | priority P0 / P1 / P2 |
| `.chip` / `.chip.o` / `.chip.new` | blue = tool, orange = open standard/protocol, outlined orange = "skill to learn" |
| `a.kw` | keyword linked to the Glossary |
| `pre.code`, `code` | code (mono font) |
| `.small` | secondary text |

Reuse existing classes; do not add CSS per handbook.

## Language and terms

- Write in **Vietnamese**, keeping technical terms in English. Sentences stay natural Vietnamese; only the term is English.
- First occurrence of a term worth remembering (reading order from Giới thiệu; the TOC does not count): `<a class="kw" href="#gl-precondition">Precondition</a> (tiền điều kiện: …)`. Every later occurrence: the English term alone, no gloss, no link. This also covers table headers, template field names and figure text.
- Not covered: everyday words (trình duyệt, người dùng, đăng nhập…) and UI labels quoted as on screen.
- Glossary: headwords are the English terms; each row `id="gl-<slug>"` (ASCII slug, `-` for other characters); the Glossary heading `id="glossary"`; sorted A–Z ignoring punctuation and spaces. The build warns about `#anchor` links without a target.
- Numbers: digits ("6 sự thật", "3 vai trò"); words only in idioms ("bên thứ ba", "cả hai") and the article "một".
- Product and service names, figures and prices change fast: verify the current name/value instead of relying on memory, and note the check date.

## Figures

One SVG file per figure, `assets/fig-NN.svg` (NN = "Hình N"); referenced as
`<figure class="fig"><img class="dia" src="assets/fig-03.svg" alt="Hình 3"><figcaption><b>Hình 3.</b> …</figcaption></figure>`.
Drawing rules: `../../../references/diagrams.md`.

## Check

1. Fix every `⚠` from the build (missing glyphs, broken anchors).
2. Render pages (`pdftoppm -r 60 -png <pdf> <prefix>`) and look at every page: no table/figure split across pages, chapters within their expected length, no near-empty pages, figures readable.
3. For a new version, compare with the previous PDF: `python3 <PLUGIN>/scripts/compare.py <new.pdf> <old.pdf>`; differences must be exactly where you edited (structural-only changes: 0 text differences, no page > 1% pixels).

## Release a version

Bump `Phiên bản Y.Z` and the month on the cover (and the quiz `version` if the topic has one), build, compare, update the status table in `course.md`. If the user keeps the course in git: commit `<COURSE> <TOPIC> vY.Z: <summary>` with a bullet list of changes by chapter/figure, tag `<COURSE>-<TOPIC>-vY.Z` — only when asked.
