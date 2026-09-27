"""Shared paths, constants, and study design choices.

Every analytic decision that affects a reported number lives here, so it can be
checked against the paper in one place.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

SEED = 20260618          # fixed seed for every bootstrap resample
N_BOOT = 5000            # bootstrap resamples for all 95% CIs

# ---------------------------------------------------------------- survey
CORE_ITEMS = {
    1: "Understood how LLM-pipeline parts fit together",
    2: "Earlier topics prepared me logically",
    3: "Clearer understanding of tokenization…integration",
    4: "Confidence explaining GPT-style systems",
    5: "Confidence evaluating LLM behavior (not just using)",
    6: "Pace appropriate for difficulty",
    7: "Workload appropriate for 3-credit course",
    8: "Quizzes/HW/project connected concepts",
    9: "Live coding labs aided understanding",
    10: "Expectations for my level were clear",
    11: "Shared UG/grad format worked well",
}
STAGES = ["Representation", "Model internals", "Training & evaluation",
          "Adaptation", "System integration"]
DIFF_ITEMS = {
    1: "UG/grad expectation differences were appropriate",
    2: "Challenged appropriately for my level",
    3: "Misconception-repair activities helped (Pipeline Debugger)",
    4: "Still uncertain how some parts connect (negatively worded)",
    5: "Emphasis on building working systems (UG only)",
    6: "Emphasis on literature/reproducibility (GR only)",
}

# ---------------------------------------------------------------- coursework
MAX_POINTS = {
    "quiz_introduction": 9, "quiz_representation": 9, "quiz_training": 9,
    "quiz_adaptation": 9, "hw1": 100, "hw2": 100, "hw3": 100,
    "milestone1": 100, "milestone2": 100, "milestone3": 100, "final_exam": 30,
}
ASSESSMENTS = list(MAX_POINTS)
COMPOSITES = {
    "quiz_avg": ["quiz_introduction", "quiz_representation", "quiz_training", "quiz_adaptation"],
    "hw_avg": ["hw1", "hw2", "hw3"],
    "milestone_avg": ["milestone1", "milestone2", "milestone3"],
}
LABELS = {
    "quiz_introduction": "Quiz: introduction", "quiz_representation": "Quiz: representation",
    "quiz_training": "Quiz: training & evaluation", "quiz_adaptation": "Quiz: adaptation",
    "hw1": "Homework 1", "hw2": "Homework 2", "hw3": "Homework 3",
    "milestone1": "Milestone 1", "milestone2": "Milestone 2", "milestone3": "Milestone 3",
    "final_exam": "Final exam", "quiz_avg": "Quiz average", "hw_avg": "Homework average",
    "milestone_avg": "Milestone average",
}

# Pre-specified confirmatory UG-vs-GR family (paper Table 7), Holm-adjusted.
CONFIRMATORY = ["hw1", "final_exam", "hw_avg", "quiz_adaptation", "milestone_avg"]

# Stage -> aligned assessments (paper RQ5; docs/assessment_mapping.md).
STAGE_ASSESSMENTS = {
    "Representation": ["quiz_representation", "hw1"],
    "Model internals": ["hw2"],
    "Training & evaluation": ["quiz_training", "hw2"],
    "Adaptation": ["quiz_adaptation", "hw3"],
    "System integration": ["hw3"],
}
