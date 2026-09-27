"""Quantitative analyses for RQ1-RQ4, reliability, and the sensitivity check.

Writes the paper's tables to results/ as CSV and every number to
results/analysis_results.json.

Note on reproducibility: all bootstrap CIs draw from ONE generator seeded with
config.SEED, in the order below (RQ1 -> RQ2 -> RQ3 -> RQ4). Reordering these
blocks changes the CIs in the second decimal place. Reliability CIs use their
own generator so they do not disturb the published values.
"""
import json
import numpy as np
import pandas as pd

import config as C
import stats as S


def load_survey():
    return pd.read_csv(C.DATA / "survey.csv")


def load_coursework(nonsubmission="zero"):
    """Percent-of-maximum scores. Excused work is blank (missing). A score of 0
    is a required but unsubmitted assignment; nonsubmission='missing' recodes
    those zeros as missing for the sensitivity analysis."""
    raw = pd.read_csv(C.DATA / "coursework.csv")
    cw = raw[["student_id", "course_level"]].copy()
    for a, mx in C.MAX_POINTS.items():
        pct = raw[a] / mx * 100
        cw[a] = pct.replace(0, np.nan) if nonsubmission == "missing" else pct
    for comp, parts in C.COMPOSITES.items():
        cw[comp] = cw[parts].mean(axis=1)
    return cw


def main():
    C.RESULTS.mkdir(exist_ok=True)
    rng = np.random.default_rng(C.SEED)
    svy, cw = load_survey(), load_coursework()
    R = {}

    # ------------------------------------------------------------ Table 4: cohort
    R["cohort"] = {
        "survey_n": len(svy),
        "survey_by_level": svy["course_level"].fillna("not reported").value_counts().to_dict(),
        "prior_llm (1=none,2=slight,3=very)": svy["prior_llm"].value_counts().sort_index().to_dict(),
        "prior_ml (1=none..4=extensive)": svy["prior_ml"].value_counts().sort_index().to_dict(),
        "acad_level (1=junior,2=senior,3=master's,4=doctoral)": svy["acad_level"].value_counts().sort_index().to_dict(),
        "coursework_n": len(cw),
        "coursework_by_level": cw["course_level"].value_counts().to_dict(),
    }
    prior_ml = svy.groupby("course_level")["prior_ml"].apply(S.describe).unstack()
    R["cohort"]["prior_ml_by_level"] = prior_ml[["n", "mean", "median"]].to_dict(orient="index")
    t4 = pd.DataFrame([
        ["Undergraduate", R["cohort"]["survey_by_level"].get("UG"), R["cohort"]["coursework_by_level"].get("UG")],
        ["Graduate", R["cohort"]["survey_by_level"].get("GR"), R["cohort"]["coursework_by_level"].get("GR")],
        ["Level not reported", R["cohort"]["survey_by_level"].get("not reported", 0), "n/a"],
        ["Prior LLM familiarity (none/slight/very)",
         " / ".join(str(v) for v in svy["prior_llm"].value_counts().sort_index()), "n/a"],
        ["Prior ML experience (none/limited/moderate/extensive)",
         " / ".join(str(v) for v in svy["prior_ml"].value_counts().sort_index()), "n/a"],
    ], columns=["characteristic", f"survey (n = {len(svy)})", f"coursework (n = {len(cw)})"])
    t4.to_csv(C.RESULTS / "table4_cohort.csv", index=False)

    # ------------------------------------------------------------ RQ1 / Figure 1
    rq1 = []
    for j, label in C.CORE_ITEMS.items():
        col = svy[f"core_{j}"]
        d = S.describe(col)
        n = d["n"]
        rq1.append(dict(item=f"core_{j}", label=label, **d,
                        pct_agree=round(100 * (col == 3).sum() / n, 1),
                        pct_neutral=round(100 * (col == 2).sum() / n, 1),
                        pct_disagree=round(100 * (col == 1).sum() / n, 1),
                        median_ci=S.boot_ci(col, np.median, rng), mean_ci=S.boot_ci(col, np.mean, rng)))
    R["RQ1_core_items"] = rq1
    pd.DataFrame(rq1).drop(columns=["median_ci", "mean_ci"]).to_csv(C.RESULTS / "rq1_core_items.csv", index=False)

    # ------------------------------------------------------------ RQ2 / Table 5, Figure 2
    rq2 = []
    for j, stage in enumerate(C.STAGES, 1):
        pair = svy[[f"before_{j}", f"now_{j}"]].dropna()
        b, a = pair[f"before_{j}"].values, pair[f"now_{j}"].values
        diff = a - b
        lo, hi = S.boot_ci(diff, np.mean, rng)
        rq2.append(dict(stage=stage, n=len(pair), before_median=float(np.median(b)),
                        now_median=float(np.median(a)), before_mean=round(float(b.mean()), 2),
                        now_mean=round(float(a.mean()), 2), mean_gain=round(float(diff.mean()), 2),
                        gain_ci_low=round(lo, 2), gain_ci_high=round(hi, 2),
                        pct_rating_higher=round(100 * float(np.mean(diff > 0)), 1),
                        pct_no_change=round(100 * float(np.mean(diff == 0)), 1),
                        pct_rating_lower=round(100 * float(np.mean(diff < 0)), 1),
                        wilcoxon_p=S.wilcoxon_p(a, b),
                        rank_biserial=round(S.rank_biserial_paired(a, b), 2)))
    R["RQ2_gains"] = rq2
    pd.DataFrame(rq2).to_csv(C.RESULTS / "table5_knowledge_gains.csv", index=False)

    # ------------------------------------------------------------ RQ3 / Table 6, Figure 3
    rq3 = []
    for a in C.ASSESSMENTS:
        d = S.describe(cw[a])
        rq3.append(dict(assessment=a, label=C.LABELS[a], **d,
                        pct_ge95=round(100 * float(np.mean(cw[a].dropna() >= 95)), 1),
                        pct_at_100=round(100 * float(np.mean(cw[a].dropna() >= 100)), 1),
                        median_ci=S.boot_ci(cw[a], np.median, rng)))
    R["RQ3_performance"] = rq3
    pd.DataFrame(rq3).drop(columns=["median_ci"]).to_csv(C.RESULTS / "table6_performance.csv", index=False)
    cw[C.ASSESSMENTS].corr(method="spearman").round(2).to_csv(C.RESULTS / "assessment_spearman_correlations.csv")

    # ------------------------------------------------------------ RQ4 / Table 7, Figure 4
    ug_s, gr_s = svy[svy.course_level == "UG"], svy[svy.course_level == "GR"]
    percep = []
    for j, label in C.CORE_ITEMS.items():
        col = f"core_{j}"
        lo, hi = S.cliffs_ci(ug_s[col].values, gr_s[col].values, rng)
        percep.append(dict(item=col, label=label, ug_median=S.describe(ug_s[col])["median"],
                           gr_median=S.describe(gr_s[col])["median"],
                           cliffs_delta=round(S.cliffs_delta(ug_s[col], gr_s[col]), 3),
                           ci_low=round(lo, 3), ci_high=round(hi, 3),
                           p_mannwhitney=S.mannwhitney_p(ug_s[col], gr_s[col])))
    R["RQ4_perceptions"] = percep
    pd.DataFrame(percep).to_csv(C.RESULTS / "rq4_perceptions_ug_vs_gr.csv", index=False)

    ug_c, gr_c = cw[cw.course_level == "UG"], cw[cw.course_level == "GR"]
    perf = {}
    for a in C.ASSESSMENTS + list(C.COMPOSITES):
        lo, hi = S.cliffs_ci(ug_c[a].values, gr_c[a].values, rng)
        perf[a] = dict(assessment=a, label=C.LABELS[a], ug_n=int(ug_c[a].notna().sum()),
                       gr_n=int(gr_c[a].notna().sum()), ug_median=round(float(ug_c[a].median()), 1),
                       gr_median=round(float(gr_c[a].median()), 1),
                       cliffs_delta=round(S.cliffs_delta(ug_c[a], gr_c[a]), 2),
                       ci_low=round(lo, 2), ci_high=round(hi, 2),
                       p_mannwhitney=S.mannwhitney_p(ug_c[a], gr_c[a]))
    R["RQ4_performance_all"] = list(perf.values())
    pd.DataFrame(perf.values()).to_csv(C.RESULTS / "rq4_performance_ug_vs_gr_all.csv", index=False)

    t7 = pd.DataFrame([perf[a] for a in C.CONFIRMATORY])
    t7["p_holm"] = S.holm(t7["p_mannwhitney"].values)
    R["table7_confirmatory"] = t7.to_dict(orient="records")
    t7.to_csv(C.RESULTS / "table7_ug_gr_confirmatory.csv", index=False)

    # Level-specific items are analyzed only for their intended group (paper,
    # Data Preparation and Analysis): diff_5 = undergraduates, diff_6 = graduates.
    intended = {5: "UG", 6: "GR"}
    diffs = []
    for j, label in C.DIFF_ITEMS.items():
        col = f"diff_{j}"
        base = svy[svy.course_level == intended[j]] if j in intended else svy
        vals = base[col].dropna()
        diffs.append(dict(item=col, label=label, analyzed_group=intended.get(j, "all"), n=int(len(vals)),
                          pct_agree=round(100 * float(np.mean(vals == 3)), 1),
                          ug_median=float(ug_s[col].median()) if ug_s[col].notna().any() else None,
                          gr_median=float(gr_s[col].median()) if gr_s[col].notna().any() else None,
                          n_answered_outside_group=int(svy[col].notna().sum() - len(vals))))
    R["RQ4_differentiation_items"] = diffs
    pd.DataFrame(diffs).to_csv(C.RESULTS / "rq4_differentiation_items.csv", index=False)

    # ------------------------------------------------------------ reliability (Methodology)
    rng_rel = np.random.default_rng(C.SEED + 1)
    rel = []
    for name, cols in [("11 core course-experience items", [f"core_{j}" for j in C.CORE_ITEMS]),
                       ("5 end-of-course ('now') knowledge ratings", [f"now_{j}" for j in range(1, 6)]),
                       ("5 retrospective 'before' knowledge ratings", [f"before_{j}" for j in range(1, 6)])]:
        x = svy[cols].dropna().values
        lo, hi = S.boot_reliability_ci(x, S.cronbach_alpha, rng_rel, C.N_BOOT)
        rel.append(dict(scale=name, n_complete=len(x), k_items=len(cols),
                        alpha=round(S.cronbach_alpha(x), 2), alpha_ci_low=round(lo, 2),
                        alpha_ci_high=round(hi, 2), omega_total=round(S.omega_total(x), 2)))
    R["reliability"] = rel
    pd.DataFrame(rel).to_csv(C.RESULTS / "reliability.csv", index=False)

    # ------------------------------------------------------------ sensitivity: non-submissions
    cw_m = load_coursework("missing")
    sens = []
    for a in C.CONFIRMATORY:
        d0 = S.cliffs_delta(cw[cw.course_level == "UG"][a], cw[cw.course_level == "GR"][a])
        d1 = S.cliffs_delta(cw_m[cw_m.course_level == "UG"][a], cw_m[cw_m.course_level == "GR"][a])
        sens.append(dict(assessment=C.LABELS[a], delta_nonsubmission_zero=round(d0, 2),
                         delta_nonsubmission_missing=round(d1, 2), abs_change=round(abs(d1 - d0), 2)))
    for a in ["hw1", "hw2", "hw3"]:
        sens.append(dict(assessment=C.LABELS[a] + " (median / mean)",
                         median_zero=float(cw[a].median()), median_missing=float(cw_m[a].median()),
                         mean_zero=round(float(cw[a].mean()), 1), mean_missing=round(float(cw_m[a].mean()), 1)))
    R["sensitivity_nonsubmission"] = sens
    pd.DataFrame(sens).to_csv(C.RESULTS / "sensitivity_nonsubmission.csv", index=False)

    json.dump(_jsonable(R), open(C.RESULTS / "analysis_results.json", "w"), indent=2)
    print("quantitative: wrote", len(list(C.RESULTS.glob("*.csv"))), "CSV tables to results/")


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if np.isnan(o) else round(float(o), 6)
    return o


if __name__ == "__main__":
    main()
