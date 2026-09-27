"""Check that the pipeline reproduces the values reported in the paper.

Run after analysis/run_all.py:
    python tests/test_reproduces_paper.py      (or: pytest tests/)
"""
import json
from pathlib import Path
import pandas as pd

RES = Path(__file__).resolve().parents[1] / "results"


def _r():
    return json.load(open(RES / "analysis_results.json"))


def test_cohort_table4():
    c = _r()["cohort"]
    assert c["survey_n"] == 45 and c["coursework_n"] == 49
    assert c["survey_by_level"] == {"GR": 23, "UG": 21, "not reported": 1}
    assert c["coursework_by_level"] == {"UG": 25, "GR": 24}


def test_rq1_agreement():
    items = {r["item"]: r for r in _r()["RQ1_core_items"]}
    assert items["core_4"]["pct_agree"] == 95.5
    assert items["core_1"]["pct_agree"] == 93.2
    assert items["core_6"]["pct_agree"] == 74.4      # pace
    assert items["core_7"]["pct_agree"] == 79.5      # workload
    assert items["core_9"]["pct_agree"] == 81.8      # live coding labs
    assert {r["n"] for r in items.values()} == {43, 44}


def test_table5_gains():
    t = pd.read_csv(RES / "table5_knowledge_gains.csv").set_index("stage")
    assert list(t.mean_gain) == [1.72, 1.50, 1.42, 1.57, 1.30]
    assert list(t.now_mean) == [2.91, 2.67, 2.79, 2.69, 2.51]
    assert list(t.pct_rating_higher) == [97.7, 97.6, 90.7, 100.0, 95.3]
    assert (t.rank_biserial == 1.0).all() and (t.wilcoxon_p < 1e-7).all()
    assert list(zip(t.gain_ci_low, t.gain_ci_high)) == [(1.56, 1.86), (1.33, 1.67), (1.21, 1.60),
                                                          (1.43, 1.71), (1.14, 1.47)]


def test_table6_performance():
    t = pd.read_csv(RES / "table6_performance.csv").set_index("assessment")
    assert t.loc["quiz_training", "median"] == 88.9 or round(t.loc["quiz_training", "median"], 1) == 88.9
    assert t.loc["quiz_training", "pct_ge95"] == 49.0
    assert t.loc["quiz_representation", "pct_ge95"] == 79.2
    assert t.loc["milestone1", "median"] == 91.0 and t.loc["milestone1", "pct_ge95"] == 20.4
    assert round(t.loc["final_exam", "median"], 1) == 94.6 and t.loc["final_exam", "min"] == 50.0
    assert t.loc["hw1", "pct_ge95"] == 79.6


def test_table7_contrasts():
    t = pd.read_csv(RES / "table7_ug_gr_confirmatory.csv").set_index("assessment")
    assert list(t.cliffs_delta) == [-0.66, -0.47, -0.43, -0.36, -0.07]
    assert (t.loc[["hw1", "final_exam", "hw_avg", "quiz_adaptation"], "p_holm"] < 0.05).all()
    assert t.loc["milestone_avg", "p_holm"] > 0.5


def test_differentiation_items():
    t = pd.read_csv(RES / "rq4_differentiation_items.csv").set_index("item")
    assert t.loc["diff_2", "pct_agree"] == 88.6
    assert t.loc["diff_3", "pct_agree"] == 84.1
    assert t.loc["diff_1", "pct_agree"] == 75.0
    assert t.loc["diff_4", "pct_agree"] == 25.0
    assert t.loc["diff_5", "pct_agree"] == 90.5      # undergraduates only
    assert t.loc["diff_6", "pct_agree"] == 91.3      # graduates only


def test_sensitivity():
    t = pd.read_csv(RES / "sensitivity_nonsubmission.csv").dropna(subset=["abs_change"])
    assert t.abs_change.max() <= 0.03


def test_rq6_themes():
    t = pd.read_csv(RES / "rq6_theme_counts.csv")
    get = lambda q, th: int(t[(t.question == q) & (t.theme == th)].respondents.iloc[0])
    assert get("most_helped", "labs") == 20 and get("most_challenging", "attention_internals") == 7
    assert get("most_challenging", "project") == 6 and get("pipeline_debugger", "dont_remember") == 5


def test_difficulty_matrix():
    t = pd.read_csv(RES / "rq5_difficulty_matrix.csv").set_index("stage")
    assert list(t.challenge_mentions) == [2, 5, 0, 0, 3]
    assert list(t.pooled_assessment_median_pct) == [100.0, 97.0, 96.5, 100.0, 97.0]


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print("ok ", t.__name__)
    print(f"All {len(tests)} checks passed.")
