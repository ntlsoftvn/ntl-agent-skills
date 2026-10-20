# Writing (shared by every NTL skill)

Rules settled over several review rounds with NTL readers. They apply to decks, documents and training material alike; a skill may add its own.

## Write for the actual reader

- Name the reader before writing (PO, customer executive, engineer, learner) and use their words. No internal jargon: a deck for the project's PO does not say "bid"; a learner handbook does not mention internal review rounds.
- Titles say what the slide or section is about, in summary form: "Summary", "Challenges 1/2: AWS services with no equivalent" — not teaser labels like "The challenge".
- Leave out what the reader will not act on (e.g. no "Decisions needed" slide unless asked). Ask before adding sections the user did not request.

## Short

- Customer documents: English unless the user asks otherwise. Training material: Vietnamese with English technical terms (see the training skill).
- Few words; fragments over full sentences on slides; one message per slide or section.
- Prefer a table, a list of 3–6 items or a diagram over a paragraph.

## Neutral, exact names

- Don't name a vendor, product or partner that is not contracted or confirmed. Say what it is ("VN Cloud", "an in-country cloud provider"), not "expected FPT".
- Call things by what they are, not by who pays: "dedicated GPU servers, bought separately", not "customer GPUs".
- Drop labels left over from internal iterations: "Lean architecture", not "Lean+"; "Extras", not "optional extras".
- Product names, features and prices change fast: verify them at writing time and say when they were checked.

## Numbers

- Digits, not number words. Estimates carry "≈" or "~" ("≈ 17.8万円/month", "~4 months").
- One currency per document, the one the reader uses (万円 for a Japanese reader; drop secondary currencies once the user picks one). State VAT and the exchange-rate date.
- Costs without a provider quote are labelled **"Reference cost"** and say where the prices come from.
- Effort: AI-assisted engineering is the default and is not called out; don't show a "traditional" figure next to it.
- Totals are stated once with their composition ("300 MD = 15 MM (280 MD core + 20 MD extras)"); rounding is part of the buffer, not a separate line.

## Consistency

- The document and its source data (estimate workbook, design doc) must agree. After every change, re-check every number that appears more than once (summary stats, roadmap totals, cost slide) and the cross-references (agenda page numbers, `N / total`, "Hình N").
- When a wording or naming decision changes in one deliverable, apply it to the companion deliverables too (deck ↔ workbook).
- Report what was changed, what was checked and what was not.
