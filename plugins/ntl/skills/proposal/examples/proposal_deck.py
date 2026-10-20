"""Example NTL proposal deck (11 slides) built on PLUGIN/scripts/ntl_deck.py. Copy this file into the work folder,
replace the CONTENT block with the real project, then:
    python3 proposal_deck.py <out.pptx> [diagram_dir]
diagram_dir holds current.png and target.png (architecture diagrams); missing files become placeholder boxes.
All content below is fictional sample text.
"""
import os
import sys

# plugin layout: <plugin>/skills/proposal/examples; standalone skill zip: <skill>/examples with shared files in <skill>/common
HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.environ.get("NTL_PLUGIN") or next(
    p for p in (os.path.abspath(os.path.join(HERE, "..", "..", "..")), os.path.abspath(os.path.join(HERE, "..", "common")))
    if os.path.exists(os.path.join(p, "scripts", "ntl_deck.py")))
sys.path.insert(0, os.path.join(PLUGIN, "scripts"))
import ntl_deck as ntl  # noqa: E402

H = ntl.H
OUT = sys.argv[1] if len(sys.argv) > 1 else "Acme_Platform_Proposal_v1.0.pptx"
IMG = sys.argv[2] if len(sys.argv) > 2 else HERE

# ============================== CONTENT ==============================
C = dict(
    project="Acme Platform Cloud Migration",
    subtitle="On-premises to managed cloud: challenges, solution, roadmap and cost",
    version="1.0", date="10/2026",
    summary=[
        ("Context", "Runs on servers in the customer's data centre; hardware support ends in 2027."),
        ("Goal", "Move to a managed cloud in-country with no change for end users."),
        ("Scope", "Web app, API, batch jobs and data. Mobile app unchanged."),
    ],
    stats=[("8 MM", "total effort (160 MD)"), ("~3 months", "to go-live (13 weeks)"), ("≈ 12万円", "per month, prd + stg infra")],
    current=[
        ("Monolith", "One Java app serves web and API"),
        ("Nightly batch", "Cron jobs on the same server"),
        ("Single database", "PostgreSQL 12, no replica"),
        ("Manual operations", "Deploys and backups by hand"),
    ],
    challenges1=[
        ("Self-hosted PostgreSQL 12", "End of life; managed service needs 15+"),
        ("Local file storage", "Files on disk: move to object storage"),
        ("Cron on the app server", "No scheduler in the target: run as jobs"),
        ("Manual deploys", "No pipeline or rollback today"),
    ],
    challenges2=[
        ("Technical", ["Upgrade PostgreSQL 12 → 16 without long downtime", "Hard-coded server paths (~40 places)", "Session state kept in memory"]),
        ("Operations and scope", ["Run monitoring and backups ourselves", "Data residency rules in-country", "Cut-over window agreed with users"]),
    ],
    solution=[
        ("Managed Kubernetes", "1 cluster; prd/stg split by namespace and node pool"),
        ("Managed services", "PostgreSQL, Object Storage, Registry"),
        ("Light self-run stack", "Prometheus/Loki, Argo CD, Sealed Secrets"),
        ("Pipeline", "Build, test and deploy on every merge"),
    ],
    points=[
        ("Containerise", "One image for web + API; batch jobs as K8s CronJobs"),
        ("Files to object storage", "Storage layer with presigned URLs"),
        ("Database upgrade", "Logical replication, short cut-over"),
        ("Stateless sessions", "Sessions in the database; scale out freely"),
        ("Config, not code", "Paths and endpoints from environment"),
        ("Safe releases", "Blue/green deploys with one-click rollback"),
    ],
    phases=[  # (name, team, from_week, to_week, MD, colour?, optional?)
        ("1. Discovery, design", "1 Architect, 1 Tech lead", 1, 2, 16, H["navy3"]),
        ("2. Platform build", "1 DevOps, 1 Dev", 3, 6, 36),
        ("3. App migration", "3 Dev", 4, 9, 72),
        ("4. SIT and acceptance", "2 Dev, 1 DevOps", 10, 12, 26),
        ("5. Go-live, handover", "1 DevOps", 13, 13, 4, H["orange"]),
        ("Hypercare (extra)", "1 DevOps", 14, 15, "extra", None, True),
    ],
    total="160 MD = 8 MM (150 MD core + 10 MD extras)",
    total_note="Includes buffer and technical risk reserve. Extras: hypercare, DR drill. Excludes waiting time (cloud contract) and PM/BrSE. W = week from kick-off.",
    cost=[("prd", "≈ 9.5"), ("stg", "≈ 2.5"), ("Total", "≈ 12.0")],
    cost_note="public price lists, provider quote pending. Incl. 10% VAT, 10/2026 exchange rate.",
    cost_plan=["W3–W9: stg only, ≈ 2.5万円/month", "W10–W13: prd + stg, ≈ 12万円/month", "During the project: ≈ 13万円"],
    cost_excl="existing licences and end-user devices.",
    chart=dict(labels=["K8s nodes", "PostgreSQL", "Object Storage", "Network (LB, IP)", "Monitoring, misc."], values=[4.6, 3.2, 1.5, 1.7, 1.0]),
    assumptions=["Provider not chosen; prices from public price lists", "Test data provided by the customer", "No change to the mobile app", "No PM/BrSE or third-party pentest; scope risks become change requests"],
    risks=[("Provider lacks a needed service", "verify in phase 1"), ("Database upgrade breaks queries", "rehearse on a copy"), ("Hidden server-path dependencies", "scan code early"), ("Load above sizing", "planned scale-out")],
)
# =====================================================================

d = ntl.create_deck(project=C["project"], doc_type="Proposal", version=C["version"], date=C["date"], total=11)
X0, XW, Y0, px, pt = d.X0, d.XW, d.Y0, d.px, d.pt
cw2, cw3 = (XW - px(28)) / 2, (XW - 2 * px(24)) / 3

d.cover(title=C["project"], subtitle=C["subtitle"])

d.agenda([("Summary", 3), ("Current architecture", 4), ("Challenges", 5), ("Solution", 7),
          ("Roadmap, team and effort", 9), ("Infrastructure cost", 10), ("Assumptions and key risks", 11)])

s = d.content("Intro", "Summary")
for i, (t, body) in enumerate(C["summary"]):
    x, y, top = X0 + i * (cw3 + px(24)), 2.15, H["orange"] if i == 1 else H["navy2"]
    d.card(s, x, y, cw3, 2.35, f"ov-{i}", top)
    d.txt(s, t, x=x + 0.25, y=y + 0.36, w=cw3 - 0.5, h=0.4, size=pt(26), bold=True, color=H["navy2"])
    d.txt(s, body, x=x + 0.25, y=y + 0.98, w=cw3 - 0.5, h=1.3, size=pt(18))
d.stats(s, C["stats"])

s = d.content("Context", "Current architecture")
d.image(s, os.path.join(IMG, "current.png"), x=X0, y=Y0, w=8.2, h=5.06, name="current-diagram")
d.numbered(s, C["current"])

s = d.content("Challenges", "Challenges 1/2: what does not move as is")
d.table(s, ["In use today", "Issue in the target"], C["challenges1"], col_w=[3.9, XW - 3.9])

s = d.content("Challenges", "Challenges 2/2: watch-outs")
for c, (t, items) in enumerate(C["challenges2"]):
    x = X0 + c * (cw2 + px(28))
    d.card(s, x, Y0, cw2, 5.2, f"ch-{c}", H["orange"] if c else H["navy2"])
    d.txt(s, t, x=x + px(26), y=Y0 + 0.3, w=cw2 - 0.6, h=0.45, size=pt(26), bold=True, color=H["navy2"])
    d.txt(s, d.bullets(items), x=x + px(26), y=Y0 + 0.95, w=cw2 - 0.55, h=4.1, size=pt(20), space_after=14)

s = d.content("Solution", "Solution: target architecture")
d.image(s, os.path.join(IMG, "target.png"), x=X0, y=Y0, w=8.6, h=4.64, name="target-diagram")
d.numbered(s, C["solution"], x=9.7, step=1.18, w=2.5, color=H["orange"], title_size=pt(18))
d.box(s, X0, 6.3, XW, 0.5, "note", "sol-note", d.lead("Scales without redesign: ", "add nodes, a DB standby or managed services.", H["navy"]))

s = d.content("Solution", "Solution: key technical points")
for i, (t, body) in enumerate(C["points"]):
    col, row = i % 3, i // 3
    x, y = X0 + col * (cw3 + px(24)), Y0 + row * 2.62
    d.card(s, x, y, cw3, 2.42, f"pt-{i}", H["orange"] if row else H["navy2"])
    d.oval(s, x + 0.25, y + 0.3, 0.42, 0.42, fill=H["navy2"], line=H["navy2"])
    d.txt(s, str(i + 1), x=x + 0.25, y=y + 0.3, w=0.42, h=0.42, size=13, bold=True, color=H["white"], align="center", valign="middle")
    d.txt(s, t, x=x + 0.8, y=y + 0.28, w=cw3 - 1.0, h=0.48, size=pt(21), bold=True, color=H["navy2"], valign="middle")
    d.txt(s, body, x=x + 0.25, y=y + 0.95, w=cw3 - 0.5, h=1.35, size=pt(18))

s = d.content("Plan and cost", "Roadmap, team and effort")
ty = d.gantt(s, weeks=16, block=4, phases=C["phases"]) + 0.15
d.box(s, X0, ty, XW, 0.62, "callout", "total", d.lead("Total effort: ", C["total"]), size=pt(21), bold=True)
d.txt(s, C["total_note"], x=X0, y=ty + 0.78, w=XW, h=0.62, size=pt(16), color=H["muted"])

s = d.content("Plan and cost", "Infrastructure cost")
d.table(s, ["Environment", "万円 / month"], C["cost"], w=5.9, col_w=[3.4, 2.5], row_h=0.52, size=pt(20))
d.txt(s, d.lead("Reference cost: ", C["cost_note"]), x=X0, y=Y0 + 2.2, w=5.9, h=0.5, size=pt(15), color=H["muted"])
d.box(s, X0, 4.15, 5.9, 1.3, "note", "plan-note")
d.txt(s, [[{"text": "Along the roadmap", "bold": True, "color": H["navy"]}]] + C["cost_plan"],
      x=X0 + 0.25, y=4.2, w=5.5, h=1.2, size=pt(18), valign="middle")
d.box(s, X0, 5.6, 5.9, 0.95, "callout", "excl", d.lead("Excluded: ", C["cost_excl"]), size=pt(18))
d.bar_chart(s, title="prd + stg cost breakdown (万円/month)", **C["chart"])

s = d.content("Assumptions and risks", "Assumptions and key risks")
d.card(s, X0, Y0, cw2, 5.25, "asm", H["navy2"])
d.txt(s, "Assumptions", x=X0 + px(26), y=Y0 + 0.3, w=cw2 - 0.6, h=0.45, size=pt(26), bold=True, color=H["navy2"])
d.txt(s, d.bullets(C["assumptions"]), x=X0 + px(26), y=Y0 + 0.95, w=cw2 - 0.55, h=4.15, size=pt(19), space_after=12)
rx = X0 + cw2 + px(28)
d.card(s, rx, Y0, cw2, 5.25, "rsk", H["orange"])
d.txt(s, "Technical risks → mitigation", x=rx + px(26), y=Y0 + 0.3, w=cw2 - 0.6, h=0.45, size=pt(26), bold=True, color=H["navy2"])
for i, (r, m) in enumerate(C["risks"]):
    y = Y0 + 0.95 + i * 0.8
    d.txt(s, r, x=rx + px(26), y=y, w=cw2 - 0.55, h=0.36, size=pt(17), bold=True, color=H["navy"])
    d.txt(s, "→ " + m, x=rx + px(26), y=y + 0.36, w=cw2 - 0.55, h=0.34, size=pt(17), color=H["orange_text"])

d.save(OUT)
