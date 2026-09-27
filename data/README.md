# Data and codebook

Two de-identified datasets from one offering of the course (Spring 2026), collected under an exempt IRB protocol. **The datasets are unlinked by design**: no identifier connects a survey response to a coursework record, so every comparison across them is at the cohort level. Row IDs (`S01`…, `C01`…, `H01`…) are arbitrary and carry no information.

| File | Contents | Rows |
|---|---|---|
| `survey.csv` | Closed-response survey items | 45 respondents |
| `coursework.csv` | Assessment scores (raw points) | 49 students |
| `open_ended_responses.json` | Open-ended survey answers, verbatim | 30 / 26 / 22 / 9 responses |
| `qualitative_coding.json` | Codebook and response-to-code assignments for the open-ended answers | — |

## De-identification

- The survey was anonymous. It collected no names, student IDs, or email addresses.
- Coursework records were de-identified after final grades were submitted.
- Released files omit survey metadata (timestamps, durations, completion flags) that is not needed for the analysis.
- Open-ended answers are stored separately from `survey.csv`, and each question's answers are in a random order, so they cannot be linked to closed-response rows or to one another. One answer that named the instructor was redacted to "[the instructor]". Otherwise, answers are verbatim, including typos.

## `survey.csv`

Analytic sample: the 45 completed responses. Of 52 students who consented, 7 did not finish (27–73% complete) and are excluded. Blank cells are unanswered items. Question wording is in [`docs/survey_instrument.md`](../docs/survey_instrument.md).

| Column | Meaning | Coding |
|---|---|---|
| `respondent_id` | Arbitrary row ID | `S01`–`S45` |
| `course_level` | Section enrolled in | `UG` undergraduate, `GR` graduate (1 blank) |
| `acad_level` | Academic level | 1 junior UG, 2 senior UG, 3 master's, 4 doctoral |
| `prior_llm` | Prior familiarity with LLMs | 1 not at all, 2 slightly, 3 very familiar |
| `prior_ml` | Prior ML / deep learning experience | 1 none, 2 limited, 3 moderate, 4 extensive |
| `core_1`–`core_11` | Core course-experience items | 1 disagree, 2 neutral, 3 agree |
| `before_1`–`before_5` | Retrospective knowledge **before** the course, by stage | 1 low, 2 moderate, 3 high |
| `now_1`–`now_5` | Knowledge **now** (end of semester), by stage | 1 low, 2 moderate, 3 high |
| `diff_1`–`diff_6` | Differentiation and misconception-repair items | 1 disagree, 2 neutral, 3 agree |

Stage order for `before_*` / `now_*`: 1 representation, 2 model internals, 3 training & evaluation, 4 adaptation, 5 system integration.

Notes:
- The scale is a deliberate three-point scale, not a collapsed five-point scale.
- `diff_4` is negatively worded ("I still feel uncertain…"); agreement is unfavorable. It is not reverse-scored in the file.
- `diff_5` was intended for undergraduates and `diff_6` for graduates, but the survey did not hide them from the other group (7 graduates answered `diff_5`; 4 undergraduates answered `diff_6`). The analysis uses only the intended group's answers.

## `coursework.csv`

| Column | Maximum points |
|---|---|
| `quiz_introduction`, `quiz_representation`, `quiz_training`, `quiz_adaptation` | 9 each |
| `hw1`, `hw2`, `hw3` | 100 each |
| `milestone1`, `milestone2`, `milestone3` | 100 each |
| `final_exam` | 30 |

`course_level` is `UG` (25) or `GR` (24). The analysis converts every score to percent of maximum.

**Special codes** (from the gradebook):
- **Blank = excused.** No submission was owed, so the item is excluded from that student's denominator.
- **0 = not submitted.** Work was owed and not received. Every 0 in the file is a non-submission. The sensitivity analysis recodes these zeros as missing.

| Item | Excused (blank) | Not submitted (0) |
|---|---|---|
| quiz_introduction | 4 | 0 |
| quiz_representation | 1 | 1 |
| quiz_training | 0 | 1 |
| quiz_adaptation | 0 | 1 |
| hw2 | 0 | 1 |
| hw3 | 0 | 2 |
| final_exam | 1 | 0 |
| all other items | 0 | 0 |

Composite scores (`quiz_avg`, `hw_avg`, `milestone_avg`) are computed in the analysis as the mean of a student's available percent scores.

## `open_ended_responses.json`

Keys: `most_helped`, `most_challenging`, `one_change`, `pipeline_debugger` (survey items 27, 28, 30, 31). Each is a list of `{response_id, text}`. Answers to item 29 (experience of the shared UG/grad structure) were not analyzed and are not released.

## `qualitative_coding.json`

The analyst's coding decisions, stored as data: for each question, the prompt, the codebook (code → definition), and the codes assigned to every response ID; the pipeline stage assigned to each "most challenging" response that names one (used in Figure 5); and the response IDs of the exemplar quotes. See [`docs/qualitative_codebook.md`](../docs/qualitative_codebook.md).
