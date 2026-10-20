# Course and topic design

Start from `templates/course.md` (course) and `templates/topic.md` (topic); copy them with `build_html.py init course|topic <dir>`.

## Structure: course → topic

| Level | Meaning |
|---|---|
| **Course** (khóa học) | A complete course for one target role, with a short UPPERCASE code (`ALLME101`, `AIQAE101`). Design doc: `course.md`. |
| **Topic** | The unit of learning, materials and release: its own objectives, materials (handbook; quiz and slides when needed) and version. Design doc: `topic.md`. |

There is no finer level: materials are made per topic. Chapters ("Chương N") are only the structure inside a handbook.

Suggested folder for a course the user keeps locally (only when they have none yet):

```
<COURSE>/course.md
<COURSE>/topics/<TOPIC>/topic.md
<COURSE>/topics/<TOPIC>/handbook/index.html (+ assets/fig-NN.svg)
<COURSE>/topics/<TOPIC>/quiz/index.html
<COURSE>/topics/<TOPIC>/slides/index.html (+ assets/)
<COURSE>/dist/                      build output to hand to learners
```

## Codes and names

- Course and topic codes are always **UPPERCASE**: folder names, file names, tags, commit subjects.
- Topic codes per course: `T01`, `T02`…, or `<Level>-<NN>` (`L0-01`, `L2-02`) when the course has levels. Special codes are allowed (`OV` overview, `00` how to learn, `-CP` checkpoint/capstone).
- A code is **never reused**. A new topic takes the next number. A content change bumps the topic's version; changed objectives mean a new topic.
- Topic names are a noun phrase of 2–5 words, without tool names or the level.

## course.md

- **Hiện trạng** (status) table: topic / content / status with version and month. Update it on every release.
- Design principles: backward design; each topic self-contained; neutral core, organisation-specific customisation kept separate; fictional examples, never real client data.
- Topic catalog with the code rules above.
- Term table (English / Vietnamese first-use gloss / slug) so wording stays consistent across topics.
- Numbered checklist per topic.
- Course-specific rules go here (e.g. "Topic 01 does not mention the content or numbering of later topics").

## topic.md

- Metadata line: level · hours · prerequisites · test-out · status and version.
- Objectives with codes (`T01.1`, `L0-01.2`…): measurable, starting with an action verb. Each question and rubric criterion maps to exactly one objective.
- Content: the handbook chapters in order, then the appendices.
- Assessment: quiz blueprint (questions per objective per attempt), minutes, pass mark; rubric when there is practical work.
- Self-assessment checklist and notes (decisions, sources, things to re-check).

## Backward design

1. Write the objectives.
2. Write the assessment: quiz blueprint and questions, rubric with pass/fail examples.
3. Write the content that lets a learner pass, and nothing the assessment and objectives do not need.

Definition of done for a topic: objectives coded, handbook built with no ⚠ warnings and every page checked, quiz `#check` clean, versions aligned, status table updated.
