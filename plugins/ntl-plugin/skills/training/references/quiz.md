# Quiz (one self-contained HTML file)

Create: `python3 <PLUGIN>/scripts/build_html.py init quiz <dir>` → `<dir>/index.html` (UI, script and a 6-question sample bank).
Publish: `python3 <PLUGIN>/scripts/build_html.py quiz <dir>/index.html --out <dist> --name NTL-<COURSE>-<TOPIC>-Quiz` → copied unchanged as `…-Quiz-vY.Z.html` (Y.Z from `"version"` in quiz-data).

## Hard rules

- **One self-contained file**: CSS, script and data inline; no CDN, no fonts or images fetched, no network calls. It must work opened via `file://` in Chrome and Safari with an empty console. Figures go inline as SVG (single quotes for attributes) or as a data URI.
- Edit **only** the `<script type="application/json" id="quiz-data">` block (and `<title>`). It is the single source of the question bank. Strings must not contain `</script>`. Formatting in stem/options/explain: `` `code` ``, `**bold**`, `\n` for a line break.
- Fields: `course`, `courseName`, `topic`, `version`, `title`, `passPct`, `minutes`, `blueprint` (objective → questions per attempt), `questions[]` with `id`, `objective`, `type` (`single` | `multi`), `stem`, `options`, `answer` (indexes), `explain`, optional `figure`, optional `retired: true`.
- Question ids `<TOPIC>-Q<NNN>` are never reused; retire a question with `"retired": true` instead of deleting or renumbering.
- Every question maps to exactly one objective. Every objective has **≥ 2 questions per attempt**, and the bank holds **≥ 3×** the questions an attempt draws for that objective.
- Pass mark 80% unless the course says otherwise; keep entry-level quizzes short (≤ 20 minutes), others ≤ 45 minutes.
- The quiz carries the same version as the topic's handbook; bump both together.
- Quizzes use the English term without a Vietnamese gloss (the handbook glossed it).

## Writing questions

- Test the objective, not trivia: prefer short scenarios ("Bạn gặp … cách làm đúng là gì?") over definitions.
- One clearly correct option (or a clear set for `multi`); distractors are plausible mistakes a learner actually makes, similar in length and form to the answer.
- `explain` says why the answer is right and why the tempting wrong options are wrong, and points to the handbook chapter.
- No "all of the above"/"none of the above"; no negative stems unless bolded (**không**).

## Check

Open the file with `#check` appended (`…/index.html#check`): the bank report lists data errors and the coverage per objective against the blueprint (3× rule). Fix every error and say which warnings remain. Then take one attempt via `file://`.
