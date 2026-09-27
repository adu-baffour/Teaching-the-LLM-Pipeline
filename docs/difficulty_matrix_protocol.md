# Topic-to-assessment mapping and difficulty-matrix protocol (RQ5, Figure 5)

The difficulty matrix compares three independent indicators of difficulty for each pipeline stage. It is built so that other instructors can repeat it in their own courses. The code is `difficulty_matrix()` in `analysis/figures.py`; the output is `results/rq5_difficulty_matrix.csv`.

## Stage-to-assessment mapping

The mapping is investigator-defined, following which assessments were taught and assessed with each stage. It is set in `STAGE_ASSESSMENTS` in `analysis/config.py`.

| Stage | Survey item | Assessments pooled |
|---|---|---|
| Representation | `before_1` / `now_1` | Representation quiz, Homework 1 (tokenizer, embeddings) |
| Model internals | `before_2` / `now_2` | Homework 2 (attention, mini-GPT) |
| Training & evaluation | `before_3` / `now_3` | Training & evaluation quiz, Homework 2 (pretraining) |
| Adaptation | `before_4` / `now_4` | Adaptation quiz, Homework 3 (LoRA) |
| System integration | `before_5` / `now_5` | Homework 3 (RAG, agents) |

Model internals and system integration have no dedicated quiz, and some homework covers two stages. This asymmetry limits stage-level comparison and is noted as a limitation.

## Protocol

For each stage:

1. **Perceived difficulty.** Mean end-of-course ("now") knowledge rating. Lower mean = harder.
2. **Qualitative salience.** Number of respondents whose "most challenging" answer names that stage. Stage assignments are stored in `data/qualitative_coding.json` under `challenge_stage_assignments`. The "attention / model internals" theme (7 respondents) splits across two stages: attention and query-key-value responses go to Model internals (5); embeddings, positional encoding, and stride go to Representation (2). RAG and agents go to System integration (3). This is why the stage counts differ from the theme counts in Figure 6.
3. **Objective difficulty.** Median percent-of-maximum across the stage's pooled assessments. Lower median = harder. Because assessments are pooled, this value can differ from a single assessment median in Table 6 (for example, the training quiz alone has a median of 88.9%, the pooled Training & evaluation value is 96.5%).
4. **Scale and display.** Min-max scale each column to 0–1 so that higher means harder (the perceived and objective columns are inverted), then draw a heat map.

**Reading the matrix.** A stage that is dark in all three columns shows convergent difficulty. A stage dark in one column and light in another shows divergence, for example model internals: high perceived difficulty with near-ceiling performance.

**Caveat.** The survey and coursework datasets are unlinked, so the matrix is a cohort-level (ecological) comparison. It cannot show whether the students who reported low confidence are the ones who scored well. Scores near the ceiling also limit how much the objective column can discriminate.
