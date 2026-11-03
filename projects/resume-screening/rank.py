"""
AI Resume Screening Helper - Step 5: Rank, shortlist and report
===============================================================
Final output a recruiter actually uses:
  * candidates sorted by score
  * a shortlist rule (score >= 60 AND no more than 1 missing must-have)
  * a CSV report and a chart that can be shared with the hiring team
The tool ASSISTS a human - it ranks and explains, a person decides.
"""
import json
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

THRESHOLD, MAX_MISSING = 60, 1
REPORT, CHART = Path("outputs/screening_report.csv"), Path("outputs/resume_scores.png")

if __name__ == "__main__":
    results = json.loads(Path("build/scores.json").read_text(encoding="utf-8"))
    df = pd.DataFrame([{
        "candidate": r["candidate"], "score": r["score"],
        "required_%": round(r["parts"]["required"] * 100),
        "missing_must_haves": ", ".join(r["missing_required"]) or "-",
        "shortlisted": (r["score"] >= THRESHOLD
                        and len(r["missing_required"]) <= MAX_MISSING),
    } for r in results]).sort_values("score", ascending=False)
    df.insert(0, "rank", range(1, len(df) + 1))

    REPORT.parent.mkdir(exist_ok=True)
    df.to_csv(REPORT, index=False)
    print(f"Shortlist rule: score >= {THRESHOLD} and <= {MAX_MISSING} missing "
          f"must-have\n")
    # Print a compact view; the full list of missing skills is in the CSV
    compact = df.assign(missing=df["missing_must_haves"].str.count(",")
                        + (df["missing_must_haves"] != "-"))
    print(compact.drop(columns="missing_must_haves").to_string(index=False))
    short = df[df["shortlisted"]]
    print(f"\nShortlisted {len(short)} of {len(df)}: "
          f"{', '.join(short['candidate'])}")
    print("Next: interview the shortlist; use the 'missing' column to plan "
          "questions.")

    # ---- Chart ----
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=120)
    order = df.iloc[::-1]
    colors = ["#30d158" if s else "#c7c7cc" for s in order["shortlisted"]]
    ax.barh(order["candidate"], order["score"], color=colors)
    ax.axvline(THRESHOLD, ls="--", lw=1, color="#ff9f0a")
    ax.text(THRESHOLD + 1, -0.45, "shortlist line", fontsize=8, color="#c77700")
    for i, v in enumerate(order["score"]):
        ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_title("Resume relevance score for 'Junior AI/ML Engineer'",
                 fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nReport: {REPORT} | Chart: {CHART}")
