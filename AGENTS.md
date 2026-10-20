# Rules for working on ntl-agent-skills

One plugin (`plugins/ntl-plugin`) serves Claude (Code, Cowork) and Codex / ChatGPT Work. Skills are written once and shared; never copy a skill per client.

## Where things go

- NTL style shared by every skill lives only at plugin level: `references/` (brand, writing, pptx, html, diagrams), `assets/` (logo, fonts, style.css), `scripts/` (ntl_deck.js, build_html.py, render.sh, setup_node.sh, compare.py, preview_svg.py). A skill never keeps its own copy of these.
- A skill is `plugins/ntl-plugin/skills/<name>/` with `SKILL.md` (front matter `name`, `description` with the trigger phrases in English and Vietnamese) and its own `references/`, `templates/`, `examples/`.
- Skills refer to shared files as `PLUGIN/…` (defined in SKILL.md as `SKILL_DIR/../..`) or with relative links (`../../../references/x.md` from a skill's reference). Keep that exact `PLUGIN` definition line: `tools/pack.py` rewrites it for the standalone zips.
- Skill text is agent-neutral: when input is needed, "ask with a question tool if the agent has one, otherwise in chat". Client-specific settings (Claude `allowed-tools`, Codex `agents/openai.yaml`) only when really needed, with the condition stated.
- New shared rules learned while making a document go into the shared references; rules for one document type go into that skill.

## Content rules

- No client names, client data or NDA material in templates, examples or references; examples are fictional.
- Templates copied from `ntl-training-hub` keep its look: after changing `assets/style.css` or a template, build the old and the new version and run `scripts/compare.py` (0 text differences, no page > 1% pixels for structural changes).

## Releasing a change

1. Check front matter, links (`python3 tools/pack.py` fails on dangling plugin links) and `claude plugin validate .`.
2. When distributed content changes, bump the version in all three places together: `.claude-plugin/marketplace.json` (plugin entry), `plugins/ntl-plugin/.claude-plugin/plugin.json`, `plugins/ntl-plugin/.codex-plugin/plugin.json`.
3. Test locally (README "Thử bản local"), then commit and push. Users update the marketplace in their app and start a new session; say that a running session does not pick up the change.
4. If fallback files are needed, run `python3 tools/pack.py` and share `dist/` (not committed).
