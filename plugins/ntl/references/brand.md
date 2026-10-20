# NTL brand (shared by every NTL skill)

## Company

From https://ntlsoft.com.vn/en/home/ (checked 10/2026; re-check before putting facts in front of a customer):

- **NTL Software JSC** (NTL Software Joint Stock Company; Japanese: NTLソフトウェア株式会社). Short form in documents: **NTL Software**.
- Founded 2007 by three co-founders. Headquarters in Hanoi, branch in Ho Chi Minh City. 100+ professionals.
- Software products and outsourcing for the Japanese and Asia–Pacific markets. Trusted partner of 50+ companies, 100+ projects delivered; the Japanese site cites 30+ AI projects.
- Japanese tagline: 「AIファーストで企業の未来を創る会社」 (an AI-first company building the future of businesses).
- Contact: contact@ntlsoft.com.vn · Address: 2nd Floor, No. 74 Khuc Thua Du, Cau Giay, Hanoi.

Use these only on an "About NTL" slide or page when the reader needs them; don't pad documents with company facts.

## Colours

The document palette (decks, handbooks, slides, diagrams). Use these hex values only.

| Role | Hex |
|---|---|
| Navy (cover background, strong text) | `14264A` |
| Navy 2 (titles, table headers) | `1F396D` |
| Navy 3 (secondary) | `3B5690` |
| Orange (accent, rules, page numbers) | `F16D22` |
| Orange text | `C9520F` |
| Light background | `F1F4FA` |
| Border | `D5DBE7` |
| Text | `1E2637` |
| Muted text | `667085` |
| Orange tint (callout background) | `FDE7D9` |
| Note background | `E9EEF7` |
| Light navy tint (bands) | `DCE3F0` |

The public website uses a brighter blue (`0C5ADB`, `0C1BAE`); documents do not.

## Logo

`PLUGIN/assets/logo.png` (on light backgrounds, 369×139) and `PLUGIN/assets/logo-white.png` (on navy, 738×474), from the website. Keep the proportions; leave clear space around it; no effects. On covers by default (white logo, top left of the deck and handbook cover).

## Fonts

DejaVu Sans and DejaVu Sans Mono (`PLUGIN/assets/fonts/`, licence in the same folder). In Office files use **Verdana** as the stand-in (same Bitstream Vera design, ships with Office).

## Layout

- **16:9 slides (decks and HTML slides):** 1280×720 px canvas (13.333×7.5 in), padding 64/80 px. Cover title 58 px, slide title 38 px, body 24 px (never below 17), footer 13 px.
  - Orange rule (84×4 px) under every slide title.
  - Footer on the left: `NTL Software · <Project or course> · <Document type>`. Page number `N / total` in bold orange on the right. No footer or number on the cover.
  - Cover: navy background, orange triangle top right, navy 3 triangle bottom right, a letter-spaced kicker (`NTL SOFTWARE · PROPOSAL`), the title, a short orange rule, a one-line subtitle, and `Version X.Y · MM/YYYY` (Vietnamese documents: `Phiên bản X.Y · Tháng MM/YYYY`) bottom left.
- **A4 handbooks:** margins 18 mm top, 16 mm sides, 22 mm bottom; sizes and components in `PLUGIN/assets/style.css`.

## Components and their meaning

| Component | Meaning |
|---|---|
| Card (light background, border, 6 px top bar) | one item of a set; navy bar normal, orange bar = emphasis |
| Note (blue tint, navy left bar) | tip, summary, neutral remark |
| Callout (orange tint, orange left bar) | principle, pitfall, exclusion, the thing not to miss |
| Numbered circle | ordered points or steps |
| Table with navy header row, thin row rules | comparisons and lists of facts |
| Big stat (orange number + muted label) | at most 3 key figures |

## File names and versions

- Customer documents: `<Project_Words_In_Title_Case>_<DocType>_v<X.Y>.<ext>`, e.g. `RoadVision_VN_Distribution_Proposal_v2.0.pptx`, `RoadVision_VN_Distribution_Estimate_v2.0.xlsx`. Every word starts with a capital; keep existing capitals (`VN`, `RoadVision`).
- Training material: `NTL-<COURSE>-<TOPIC>-<Handbook|Slides|Quiz>-vY.Z`, workshops `NTL-Workshop-<Title-Words>-Slides-vY.Z`.
- The version in the file name always equals the version on the cover. Before choosing a version, ask whether earlier versions exist (a document may continue from an older line, e.g. start at v2.0). Documents that belong together (a deck and its estimate workbook) carry the same version.
