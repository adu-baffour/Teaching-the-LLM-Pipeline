# Teaching Large Language Models: Code, Data, and Materials

Reproducibility package for:

> Baffour, A. A. (2026). Teaching large language models: A pipeline-centered course design and mixed-methods evidence from a cross-listed undergraduate/graduate offering. *Journal of Information Technology Education: Innovations in Practice*. (In press)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22994928.svg)](https://doi.org/10.5281/zenodo.22994928)

**Archived copy:** Zenodo, https://doi.org/10.5281/zenodo.22994928

The repository contains the de-identified data, the analysis code that regenerates every table, figure, and statistic in the paper, and the reusable course and evaluation materials (survey instrument, qualitative codebook, difficulty-matrix protocol, and Pipeline Debugger template).

## Quick start

Requires Python 3.9 or later.

```bash
pip install -r requirements.txt
python analysis/run_all.py            # writes results/ and figures/
python tests/test_reproduces_paper.py  # checks the outputs against the paper
```

All bootstrap confidence intervals use a fixed seed (`analysis/config.py`), so the outputs are identical on every run. The notebook `notebooks/reproduce.ipynb` does the same and displays the figures.

## Where each part of the paper comes from

| Paper | Output file | Produced by |
|---|---|---|
| Table 4 (cohort) | `results/table4_cohort.csv` | `analysis/quantitative.py` |
| Survey reliability (Cronbach's α, McDonald's ω) | `results/reliability.csv` | `analysis/quantitative.py` |
| RQ1, Figure 1 | `results/rq1_core_items.csv`, `figures/figure1_core_items.png` | `quantitative.py`, `figures.py` |
| RQ2, Table 5, Figure 2 | `results/table5_knowledge_gains.csv`, `figures/figure2_knowledge_gains.png` | `quantitative.py`, `figures.py` |
| RQ3, Table 6, Figure 3 | `results/table6_performance.csv`, `figures/figure3_performance.png` | `quantitative.py`, `figures.py` |
| RQ4, Table 7, Figure 4 | `results/table7_ug_gr_confirmatory.csv`, `results/rq4_*.csv`, `figures/figure4_ug_vs_gr.png` | `quantitative.py`, `figures.py` |
| Sensitivity analysis (non-submissions) | `results/sensitivity_nonsubmission.csv` | `quantitative.py` |
| RQ5, Figure 5 (difficulty matrix) | `results/rq5_difficulty_matrix.csv`, `figures/figure5_difficulty_matrix.png` | `figures.py` |
| RQ6, Figure 6 (themes) | `results/rq6_theme_counts.csv`, `results/rq6_audit_trail.csv`, `figures/figure6_themes.png` | `qualitative.py`, `figures.py` |

`results/analysis_results.json` holds every computed value, including the ones not shown in tables (bootstrap CIs for each item, Spearman correlations, UG/GR contrasts for all assessments).

## Repository layout

```
├── analysis/
│   ├── config.py           # paths, seed, item labels, stage-to-assessment mapping, confirmatory family
│   ├── stats.py            # nonparametric tests, Cliff's delta, bootstrap, Holm, alpha, omega (NumPy only)
│   ├── quantitative.py     # RQ1–RQ4, reliability, sensitivity analysis
│   ├── qualitative.py      # RQ6 theme counts and audit trail
│   ├── figures.py          # Figures 1–6 and the RQ5 difficulty matrix
│   └── run_all.py          # runs the three steps in order
├── data/                   # de-identified inputs + codebook (see data/README.md)
├── docs/                   # course design, survey instrument, codebooks, protocols
├── figures/                # Figures 1–6 (PNG, 300 dpi)
├── notebooks/reproduce.ipynb
├── results/                # generated tables (CSV) and analysis_results.json
└── tests/test_reproduces_paper.py
```

## Materials for instructors and researchers

- [Course design](docs/course_design.md): the pipeline-centered sequence, aligned assessments, and UG/GR differentiation.
- [Survey instrument](docs/survey_instrument.md): the anonymous end-of-semester survey as deployed.
- [Qualitative codebook](docs/qualitative_codebook.md): themes, definitions, and counts for the open-ended items.
- [Difficulty-matrix protocol](docs/difficulty_matrix_protocol.md): the stage-to-assessment mapping and how to build the triangulation matrix for another course.
- [Pipeline Debugger](docs/pipeline_debugger.md): the misconception-repair activity template (a proposed intervention, not evaluated in the paper).

## Study design notes

- **Unlinked data.** The anonymous survey (n = 45) and the coursework records (n = 49) cannot be linked at the individual level. Cross-source comparisons (RQ5) are cohort-level only.
- **Self-reported gains.** Knowledge gains (RQ2) come from a retrospective before/now self-rating in a single end-of-semester survey. They measure perceived, not demonstrated, learning.
- **Ceiling effects.** Most quiz and homework scores fall between 97% and 100%, which limits how well the assessments separate stronger students.
- **Analysis choices.** Ordinal data, modest samples, and ceiling effects led to effect sizes with 95% percentile bootstrap CIs (5,000 resamples), Wilcoxon signed-rank and Mann–Whitney tests (normal approximation with tie and continuity corrections), and Holm correction across the five pre-specified UG/GR comparisons. Everything else is exploratory.
- **Raw data.** The raw survey export and gradebook contain identifiers and are not distributed. `data/README.md` documents every cleaning rule applied to them.

## How to cite

Please cite the paper. To cite this package directly, use the Zenodo DOI above or GitHub's "Cite this repository" button.

## License

Code: MIT (see `LICENSE`). Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
