# Workshop (script + slides)

A one-off workshop or talk outside a course. Folder = ASCII kebab-case slug of the workshop name (`chatgpt-work-case-study/`), holding `workshop.md` and `slides/`.

Create: `build_html.py init workshop <dir>` (→ `workshop.md`) and `build_html.py init slides <dir>/slides`.

## workshop.md

Follow `templates/workshop.md`:

1. One paragraph: length, audience, what the audience already knows, what is out of depth.
2. Status line (draft / reviewed) and who presents.
3. **Mục tiêu buổi**: 3 outcomes the audience can do afterwards; one line on what is out of scope.
4. **Ba ý chính**: the 3 ideas the presenter keeps returning to.
5. **Kịch bản**: preparation, then parts with minutes (≈ n phút), each saying what is done, said and shown. Use fictional data, or data the owner allowed; never real client names on slides.
6. **Dàn slide**: table # / slide / content / image / minutes; the minutes add up to the slot.
7. **Lời dẫn gợi ý** per slide (the same text goes into `<aside class="notes">`).
8. **Cần kiểm lại trước buổi**: product names, features and prices valid on the day; slides built and checked; minutes match.

Mermaid is fine for diagrams inside `workshop.md`; slide figures are SVG files (`diagrams.md`).

## Slides

Build and check them as in `slides.md`, with `--name NTL-Workshop-<Title-Words>-Slides`.
