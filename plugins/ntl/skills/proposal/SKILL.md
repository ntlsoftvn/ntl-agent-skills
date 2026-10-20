---
name: proposal
description: Make or revise an NTL Software proposal deck (.pptx) in NTL style for a PO, customer or manager - context and current architecture, challenges, solution architecture and key technical points, roadmap with team and effort, infrastructure cost, assumptions and risks. Use for requests such as "make a proposal", "proposal deck", "proposal slides for the PO", "soạn proposal", "làm slide đề xuất", "làm deck proposal theo style NTL", "deck cho PO", "cập nhật proposal", "lên version proposal", or when an estimate or design must be turned into slides for a customer.
---

# NTL proposal deck

A short, visual proposal deck in the NTL house style, built as a real .pptx with a script so it can be rebuilt after every review round.

## Paths

- `SKILL_DIR`: the folder containing this `SKILL.md`.
- `PLUGIN`: `SKILL_DIR/../..` (the plugin root): shared style in `PLUGIN/references/`, logos and fonts in `PLUGIN/assets/`, tools in `PLUGIN/scripts/`.

## Workflow

1. **Inputs.** Ask for what is missing (question tool if the agent has one, otherwise chat) and echo the answers back before building:
   - project name and the reader (PO, customer executive, …), language (default English);
   - version (ask whether earlier versions exist), month/year for the cover;
   - output folder; never guess it;
   - source material: estimate workbook, architecture notes, diagrams, cost sheet. Numbers come from these sources, never invented.
2. **Read** `PLUGIN/references/brand.md`, `PLUGIN/references/writing.md`, `PLUGIN/references/pptx.md`, then `references/structure.md` and `references/decisions.md`.
3. **Outline** the slides from `structure.md` (title + one-line message each) and show it to the user when the request is new; keep to the slide budgets.
4. **Setup** Python once as in `pptx.md` (`setup_python.sh`, after telling the user it downloads the python-pptx package, if it is not installed).
5. **Build script.** Copy `examples/proposal_deck.py` to the work folder as `build_deck.py`, set `NTL_PLUGIN` or keep the relative `PLUGIN` path, and replace the CONTENT block. Diagrams: SVG per `PLUGIN/references/diagrams.md`, exported to PNG.
6. **Build and check.** Build, render with `render.sh`, look at every slide, fix, rebuild. Run the validator if available.
7. **Cross-check numbers**: summary stats = roadmap total = cost slide = source workbook; agenda pages and `N / total` match the slides.
8. **Name and deliver**: `<Project_Words_In_Title_Case>_Proposal_v<X.Y>.pptx` in the output folder. Report the path, the version, what was checked (and what was not, e.g. charts not visible in Keynote).

## Revisions

Edit the CONTENT block of `build_deck.py`, never the .pptx. Apply wording decisions everywhere they occur (deck and companion workbook), bump the version only when the user asks for a new version, and re-run steps 6–8.
