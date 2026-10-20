---
name: training
description: Design, write, build and release NTL Software training material in NTL style - course and topic design (course.md, topic.md, objectives, assessment), topic handbooks (HTML source to A4 PDF), HTML slide decks for workshops and topics, self-contained quiz pages, and workshop scripts. Use for requests such as "thiết kế khóa học", "mở khóa học mới", "tạo topic mới", "soạn handbook", "viết tài liệu đào tạo", "sửa chương 3", "thêm hình", "vẽ lại Hình 5", "build PDF", "check ngắt trang", "so với bản cũ", "lên v1.1", "thêm thuật ngữ vào Glossary", "tạo quiz", "thêm câu hỏi", "làm slide", "soạn slide workshop", "xuất slide PDF", "design a training course", "write a handbook", "make workshop slides", "build a quiz".
---

# NTL training material

Training material of NTL Software, made the way the ntl-training-hub repo makes it, but in any folder the user chooses. A topic's **handbook HTML is the single source of truth**; PDFs and built slides are derived files and are never edited by hand.

## Paths

- `SKILL_DIR`: the folder containing this `SKILL.md`. Templates are in `SKILL_DIR/templates/`, rules in `SKILL_DIR/references/`.
- `PLUGIN`: `SKILL_DIR/../..` (the plugin root). Shared NTL style is in `PLUGIN/references/`, `PLUGIN/assets/`, and tools in `PLUGIN/scripts/`.

## Before anything

1. Ask for what is missing (with a question tool if the agent has one, otherwise in chat), then echo the answers back:
   - what to make: course design, topic design, handbook, slides, quiz, workshop, or a new version of one of them;
   - the **working folder** (where sources live) and the **output folder** (where PDFs go); never guess them from the current directory;
   - course code and topic code (UPPERCASE), course and topic names, version, audience, language (default: Vietnamese with English technical terms);
   - source material (notes, documents, existing handbook).
2. Read `PLUGIN/references/brand.md`, `PLUGIN/references/writing.md`, `PLUGIN/references/html.md`, and `PLUGIN/references/diagrams.md` before drawing figures.
3. Check tools once: `python3`, Google Chrome (or Chromium; `CHROME=/path` if elsewhere). Optional: poppler (`pdftotext`, `pdftoppm`) or `pip install pypdf` for table-of-contents numbers; `pip install fonttools` for glyph checks; `pip install pillow` for `compare.py`. Say what is missing and what it costs (e.g. "no page numbers in the TOC") instead of failing silently.

## Routes

| Request | Read | Start from |
|---|---|---|
| Design a course | `references/course-design.md` | `build_html.py init course <dir>` |
| Design a topic | `references/course-design.md` | `build_html.py init topic <dir>` |
| Write or edit a handbook | `references/handbook.md` | `build_html.py init handbook <dir>` |
| Slides for a talk or topic | `references/slides.md` | `build_html.py init slides <dir>` |
| Quiz | `references/quiz.md` | `build_html.py init quiz <dir>` |
| Workshop | `references/workshop.md` (+ `slides.md`) | `build_html.py init workshop <dir>` |
| New version / release | `references/handbook.md` § Release | the existing source |

`build_html.py` is `python3 PLUGIN/scripts/build_html.py`; run it with `--help` for every command. `init` never overwrites an existing file unless given `--force`.

## Working rules

- Objectives first (backward design): objectives → assessment → content. Each question or rubric criterion maps to one objective.
- Keep each figure in its own `assets/fig-NN.svg`; "Hình N" numbering matches the file names.
- Use only the classes of the shared stylesheet; do not edit `ntl-assets/style.css` in a document folder.
- Verify product names, figures and prices before writing them; note the date checked.
- Never put client data or names in examples; use fictional examples.

## Done means

1. The build ran with no `⚠` warnings left unexplained.
2. You looked at the rendered pages (`pdftoppm -r 60 -png …`, then read the images): no table or figure split across pages, no overflow, no near-empty page or slide.
3. Quiz: `#check` shows no errors; versions of handbook and quiz match.
4. Report the output files (full paths), the version, what you checked, and anything not checked.
