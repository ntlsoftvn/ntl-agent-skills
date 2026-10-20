# Proposal deck structure

Default: **11 slides** for a technical proposal (migration, new system, re-platforming) read by a PO or a customer manager. One message per slide. Budgets set by NTL reviewers: problems ≤ 2 slides, solution ≤ 2 (one high level, one low level), estimate + schedule + team on **1** slide, infrastructure cost on **1** slide.

| # | Section | Slide | Content | Example builder call |
|---|---|---|---|---|
| 1 | Intro | Cover | Kicker `NTL SOFTWARE · PROPOSAL`, project name (title case), one-line subtitle ("From X to Y: challenges, solution, roadmap and cost"), `Version X.Y · MM/YYYY` | `d.cover` |
| 2 | Intro | Agenda | Numbered sections with their start page | `d.agenda` |
| 3 | Intro | Summary | 3 cards: Context / Goal / Scope (one or two lines each); 3 big stats: total effort (MM + MD), time to go-live, monthly infrastructure cost | `d.card`, `d.stats` |
| 4 | Context | Current architecture | High-level diagram of today's system + 4 numbered points (what matters for the change) | `d.image`, `d.numbered` |
| 5 | Challenges | Challenges 1/2: <headline> | Table: what is used today → the issue in the target | `d.table` |
| 6 | Challenges | Challenges 2/2: watch-outs | 2 cards: Technical / Operations and scope, 3–4 bullets each | `d.card`, `d.bullets` |
| 7 | Solution | Solution: <name> architecture | Target diagram + 4 numbered points + a note ("Scales without redesign: …") | `d.image`, `d.numbered`, `d.box` |
| 8 | Solution | Solution: key technical points | 6 cards (2 rows × 3): how each challenge is solved | `d.card` |
| 9 | Plan and cost | Roadmap, team and effort | Gantt in 4-week blocks with a line per week, team per phase, MD per phase; callout "Total effort: X MD = Y MM (A MD core + B MD extras)"; one muted line on what is included/excluded | `d.gantt`, `d.box` |
| 10 | Plan and cost | Infrastructure cost | Environment table (one currency); "Reference cost: …" line; "Along the roadmap" note (cost per period and during the project); exclusions callout; breakdown bar chart | `d.table`, `d.box`, `d.barChart` |
| 11 | Assumptions and risks | Assumptions and key risks | 2 cards: assumptions (bullets) / technical risks → mitigation | `d.card` |

Optional, only when asked or clearly needed: **About NTL** (facts from `brand.md`), a team slide, a references slide. Do not add a "Decisions needed" or "Next steps" slide unless the user asks.

Section headers for the pptx sections: Intro · Context · Challenges · Solution · Plan and cost · Assumptions and risks.

## Writing each slide

- Title = the message ("Challenges 1/2: AWS services with no equivalent"), not a teaser.
- Cards and points: a bold 2–4 word label + one line. Bullets: ≤ 6 per card, one line each where possible.
- Every number shown appears in the source data (estimate workbook, cost sheet) with the same value and rounding.
- Diagrams are high level: one box per service or group, labelled arrows, the new or risky part in orange.
