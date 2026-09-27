"""RQ6: theme frequencies from the reflexive thematic analysis.

The coding decisions (codebook, response-to-code assignments, stage
assignments, exemplar quotes) are analyst judgments and are stored as data in
data/qualitative_coding.json. This script only counts them and writes a
readable audit trail.
"""
import json
from collections import Counter
import pandas as pd

import config as C


def load():
    responses = json.load(open(C.DATA / "open_ended_responses.json", encoding="utf-8"))
    coding = json.load(open(C.DATA / "qualitative_coding.json", encoding="utf-8"))
    return responses, coding


def theme_counts(responses, coding):
    rows = []
    for q, spec in coding["questions"].items():
        ids = {r["response_id"] for r in responses[q]}
        assert set(spec["assignments"]) == ids, f"{q}: every response must be coded exactly once"
        counts = Counter(code for codes in spec["assignments"].values() for code in codes)
        for code, n in counts.most_common():
            rows.append(dict(question=q, n_responses=len(ids), theme=code, respondents=n,
                             definition=spec["codebook"][code]))
    return pd.DataFrame(rows)


def challenge_mentions_by_stage(coding):
    stages = {k: v for k, v in coding["challenge_stage_assignments"].items() if not k.startswith("_")}
    counts = Counter(stages.values())
    return {s: counts.get(s, 0) for s in C.STAGES}


def main():
    C.RESULTS.mkdir(exist_ok=True)
    responses, coding = load()
    df = theme_counts(responses, coding)
    df.to_csv(C.RESULTS / "rq6_theme_counts.csv", index=False)

    text = {r["response_id"]: r["text"] for q in responses for r in responses[q]}
    stages = coding["challenge_stage_assignments"]
    trail = []
    for q, spec in coding["questions"].items():
        for rid, codes in spec["assignments"].items():
            trail.append(dict(question=q, response_id=rid, codes="; ".join(codes) or "(none)",
                              pipeline_stage=stages.get(rid, ""), response=text[rid]))
    pd.DataFrame(trail).to_csv(C.RESULTS / "rq6_audit_trail.csv", index=False)
    pd.Series(challenge_mentions_by_stage(coding), name="challenge_mentions").rename_axis("stage") \
        .to_csv(C.RESULTS / "rq5_challenge_mentions_by_stage.csv")
    print("qualitative: wrote theme counts, audit trail, and stage mentions to results/")


if __name__ == "__main__":
    main()
