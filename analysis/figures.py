"""Figures 1-6 and the difficulty matrix (RQ5).

Figure titles are not drawn on the images: the paper sets figure numbers and
titles above each figure in APA style. Output: figures/*.png at 300 dpi.
Run quantitative.py and qualitative.py first (run_all.py does this).
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import config as C
from quantitative import load_coursework
from qualitative import load, theme_counts, challenge_mentions_by_stage

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 300, "savefig.bbox": "tight"})
C_DIS, C_NEU, C_AGR = "#D55E00", "#CCCCCC", "#0072B2"   # colorblind-safe (Okabe-Ito)
C_UG, C_GR = "#E69F00", "#009E73"


def fig1(R):
    items = R["RQ1_core_items"]
    order = np.argsort([it["pct_agree"] for it in items])
    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    for y, i in enumerate(order):
        it = items[i]
        dis, neu, agr = it["pct_disagree"], it["pct_neutral"], it["pct_agree"]
        ax.barh(y, neu, left=-neu / 2, color=C_NEU, edgecolor="white")
        ax.barh(y, agr, left=neu / 2, color=C_AGR, edgecolor="white")
        ax.barh(y, -dis, left=-neu / 2, color=C_DIS, edgecolor="white")
        ax.text(neu / 2 + agr + 1, y, f"{agr:.0f}%", va="center", fontsize=9, color=C_AGR)
    ax.axvline(0, color="#444", lw=0.8)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([items[i]["label"] for i in order], fontsize=10)
    ax.set_xlim(-30, 110)
    ax.set_xlabel("Percent of respondents (Disagree left of zero, Agree right)")
    ax.legend(handles=[Patch(color=C_DIS, label="Disagree"), Patch(color=C_NEU, label="Neutral"),
                       Patch(color=C_AGR, label="Agree")], loc="lower right", frameon=False, fontsize=9)
    fig.savefig(C.FIGURES / "figure1_core_items.png")
    plt.close(fig)


def _spread(values, gap):
    """Return label positions that keep labels at least `gap` apart, preserving order."""
    order = sorted(range(len(values)), key=lambda k: -values[k])
    pos, prev = {}, None
    for k in order:
        y = values[k] if prev is None else min(values[k], prev - gap)
        pos[k] = y
        prev = y
    return pos


def fig2(R):
    g = R["RQ2_gains"]
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    before, now = [r["before_mean"] for r in g], [r["now_mean"] for r in g]
    lb, ln = _spread(before, 0.11), _spread(now, 0.11)
    for k, r in enumerate(g):
        col = plt.cm.viridis(k / 5)
        ax.plot([0, 1], [r["before_mean"], r["now_mean"]], "-o", color=col, lw=2.2, ms=7)
        ax.plot([-0.03, -0.09], [r["before_mean"], lb[k]], color=col, lw=0.8)
        ax.text(-0.11, lb[k], f'{r["before_mean"]:.2f}  {r["stage"]}', ha="right", va="center",
                fontsize=11, color=col)
        ax.text(1.05, ln[k], f'{r["now_mean"]:.2f}  {r["stage"]}', ha="left", va="center",
                fontsize=11, color=col)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Before the course\n(rated retrospectively)", "Now\n(end of semester)"], fontsize=11)
    ax.set_xlim(-0.95, 1.85)
    ax.set_ylim(0.5, 3.25)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low (1)", "Moderate (2)", "High (3)"], fontsize=12)
    ax.set_ylabel("Mean self-rated knowledge", fontsize=12)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    fig.savefig(C.FIGURES / "figure2_knowledge_gains.png")
    plt.close(fig)


def fig3(cw, R):
    data = [cw[a].dropna().values for a in C.ASSESSMENTS]
    fig, ax = plt.subplots(figsize=(11.5, 5.4))
    bp = ax.boxplot(data, widths=0.6, patch_artist=True, showfliers=False)
    for b in bp["boxes"]:
        b.set(facecolor="#D9E8F5", edgecolor="#2E75B6")
    for m in bp["medians"]:
        m.set(color="#C00000", lw=1.8)
    for k, d in enumerate(data, 1):
        ax.scatter(np.random.default_rng(k).normal(k, 0.07, len(d)), d, s=10, color="#333", alpha=0.45, zorder=3)
    rep = next(r for r in R["RQ3_performance"] if r["assessment"] == "quiz_representation")
    k = C.ASSESSMENTS.index("quiz_representation") + 1
    ax.annotate(f"{rep['pct_at_100']:.0f}% scored 100%:\nbox collapses to a\nline at the ceiling",
                xy=(k, 99), xytext=(k + 0.3, 28), fontsize=9, ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#bbb", lw=0.6),
                arrowprops=dict(arrowstyle="->", color="#555", lw=0.9))
    ax.set_xticks(range(1, len(C.ASSESSMENTS) + 1))
    short = {"quiz_introduction": "Quiz:\nintro", "quiz_representation": "Quiz:\nrepresent.",
             "quiz_training": "Quiz:\ntrain & eval", "quiz_adaptation": "Quiz:\nadaptation",
             "hw1": "HW 1", "hw2": "HW 2", "hw3": "HW 3", "milestone1": "Mile-\nstone 1",
             "milestone2": "Mile-\nstone 2", "milestone3": "Mile-\nstone 3", "final_exam": "Final\nexam"}
    ax.set_xticklabels([short[a] for a in C.ASSESSMENTS], fontsize=9)
    ax.set_ylabel("Percent of maximum")
    ax.set_ylim(-3, 106)
    fig.savefig(C.FIGURES / "figure3_performance.png")
    plt.close(fig)


def fig4(cw):
    keys = ["quiz_avg", "hw_avg", "milestone_avg", "final_exam"]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for j, k in enumerate(keys):
        for off, lvl, fc, dc, s in [(-0.18, "UG", C_UG, "#7a5600", j), (0.18, "GR", C_GR, "#005c43", j + 9)]:
            v = cw[cw.course_level == lvl][k].dropna()
            b = ax.boxplot(v, positions=[j + off], widths=0.3, patch_artist=True, showfliers=False)
            for box in b["boxes"]:
                box.set(facecolor=fc, alpha=0.7)
            for m in b["medians"]:
                m.set(color="#222", lw=1.5)
            ax.scatter(np.random.default_rng(s).normal(j + off, 0.04, len(v)), v, s=9, color=dc, zorder=3)
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels([C.LABELS[k] for k in keys])
    ax.set_ylabel("Percent of maximum")
    n_ug, n_gr = (cw.course_level == "UG").sum(), (cw.course_level == "GR").sum()
    ax.legend(handles=[Patch(color=C_UG, label=f"Undergraduate (n = {n_ug})"),
                       Patch(color=C_GR, label=f"Graduate (n = {n_gr})")],
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=10)
    fig.savefig(C.FIGURES / "figure4_ug_vs_gr.png")
    plt.close(fig)


def difficulty_matrix(cw, R, coding):
    now = np.array([next(r["now_mean"] for r in R["RQ2_gains"] if r["stage"] == s) for s in C.STAGES])
    chal = np.array([challenge_mentions_by_stage(coding)[s] for s in C.STAGES], float)
    perf = np.array([np.nanmedian(pd.concat([cw[a] for a in C.STAGE_ASSESSMENTS[s]])) for s in C.STAGES])
    norm = lambda a: (a - a.min()) / (a.max() - a.min() + 1e-9)
    M = np.vstack([1 - norm(now), norm(chal), 1 - norm(perf)]).T
    tab = pd.DataFrame({"stage": C.STAGES, "now_mean": now, "challenge_mentions": chal.astype(int),
                        "pooled_assessment_median_pct": perf.round(1),
                        "assessments_pooled": [", ".join(C.STAGE_ASSESSMENTS[s]) for s in C.STAGES],
                        "difficulty_perceived": M[:, 0].round(2), "difficulty_qualitative": M[:, 1].round(2),
                        "difficulty_objective": M[:, 2].round(2)})
    tab.to_csv(C.RESULTS / "rq5_difficulty_matrix.csv", index=False)
    return now, chal, perf, M


def fig5(now, chal, perf, M):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    im = ax.imshow(M, cmap="OrRd", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["Perceived\n(mean 'now' rating)", "Qualitative\n(challenge mentions)",
                        "Objective\n(median % of max)"], fontsize=10)
    ax.set_yticks(range(5))
    ax.set_yticklabels(C.STAGES, fontsize=10.5)
    for i in range(5):
        for j, t in enumerate([f"{now[i]:.2f}", f"{int(chal[i])}", f"{perf[i]:.1f}%"]):
            ax.text(j, i, t, ha="center", va="center", fontsize=10, color="white" if M[i, j] > 0.6 else "#333")
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.set_label("Relative difficulty (0 = easiest, 1 = hardest)", fontsize=9)
    fig.savefig(C.FIGURES / "figure5_difficulty_matrix.png")
    plt.close(fig)


def fig6(tc):
    pretty = {"labs": "Live coding labs", "instructor": "Instructor explanations", "structure": "Course structure",
              "project": "Project", "visualization": "Visual representations", "homework": "Homework",
              "attention_internals": "Attention / model internals", "labs_tooling": "Labs pace / tooling",
              "rag_agents": "RAG / agents", "pace": "Pace", "ml_background": "ML background",
              "interconnections": "Interacting concepts"}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    for ax, q, col, title in [(axes[0], "most_helped", C_AGR, "What most helped learning"),
                              (axes[1], "most_challenging", C_DIS, "Most challenging or least clear")]:
        d = tc[tc.question == q].iloc[::-1]
        ax.barh([pretty.get(t, t) for t in d.theme], d.respondents, color=col, alpha=0.85)
        for i, v in enumerate(d.respondents):
            ax.text(v + 0.2, i, str(v), va="center", fontsize=9)
        ax.set_title(f"{title} (n = {d.n_responses.iloc[0]})", fontsize=11, loc="left")
        ax.set_xlabel("Respondents")
    fig.tight_layout()
    fig.savefig(C.FIGURES / "figure6_themes.png")
    plt.close(fig)


def main():
    C.FIGURES.mkdir(exist_ok=True)
    R = json.load(open(C.RESULTS / "analysis_results.json"))
    cw = load_coursework()
    responses, coding = load()
    fig1(R)
    fig2(R)
    fig3(cw, R)
    fig4(cw)
    fig5(*difficulty_matrix(cw, R, coding))
    fig6(theme_counts(responses, coding))
    print("figures: wrote", sorted(p.name for p in C.FIGURES.glob("*.png")))


if __name__ == "__main__":
    main()
