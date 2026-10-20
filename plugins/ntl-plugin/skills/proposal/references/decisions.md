# Proposal decisions (settled in review; apply unless the user says otherwise)

## Effort and schedule

- Effort is estimated for engineers working with AI agents; this is the default and is **not** mentioned on the slides, and no "traditional" figure is shown.
- One total, stated with its composition: "300 MD = 15 MM (280 MD core + 20 MD extras)". 1 MM = 20 MD.
- The total **includes** a buffer and a technical-risk reserve (expected value of the technical risks). Rounding up to whole MM is part of the buffer, never a separate line. Say this in one muted line under the total.
- Scope and dependency risks (requirement changes, customer approvals) are **change requests**, not reserve.
- The total **excludes** waiting time (cloud contract, hardware delivery, approvals) and PM/BrSE unless the user includes them. Say so.
- Scope split: **core** (needed to go live) and **extras** (hypercare, DR drill, autoscaling, WAF rule set…). Label them "Extras", not "optional extras". Hypercare is shown in the Gantt as an extra row in a lighter colour.
- Phase MD on the roadmap add up exactly to the core total; the extras row shows "extra" (or its MD) and the callout gives both.
- Time to go-live in weeks and roughly in months ("~4 months / 17 weeks"); W = week from kick-off.

## Cost

- Infrastructure cost per month per environment (prd, stg) and the total, in the reader's currency only (万円 for a Japanese PO). Show "≈" values with one decimal.
- Label: "Reference cost: public price lists, provider quote pending. Incl. 10% VAT, MM/YYYY exchange rate." until a provider quote exists.
- Add "Along the roadmap": which environments run in which weeks, cost per month in each period, and the total during the project.
- Exclusions in an orange callout, e.g. "GPU excluded: separate purchase; GPU prices are volatile now."
- Lean by default: estimate the architecture that is chosen, not scale-up or optional add-on variants; mention that it scales without redesign.

## Wording for the PO reader

- No "bid", "tender" or internal estimating terms; the deck is a proposal.
- Don't name a cloud provider or vendor that is not contracted ("VN Cloud", "in-country cloud provider (not fixed yet)").
- Things the customer buys separately are described as such ("dedicated GPU servers, bought separately"), not as "customer GPUs".
- Keep internal iteration names out ("Lean architecture", not "Lean+").

## Deliverables

- File name `<Project_Words_In_Title_Case>_Proposal_v<X.Y>.pptx`; the cover shows the same name (title case) and version. Companion workbook: `<Project…>_Estimate_v<X.Y>.xlsx`, same version.
- When the deck changes wording, names or numbers, update the companion workbook the same way (and the reverse), then re-check both.
