"""
Student Performance Prediction - Step 6: Predict for new students
=================================================================
How the model is used in practice: a teacher enters a student's details,
we apply EXACTLY the same preprocessing as in training, and the model
returns the probability of passing plus a risk label.

Re-using preprocess() from step 2 is important - if training and prediction
encoded data differently, the model would silently give wrong answers.
"""
from pathlib import Path

import joblib
import matplotlib
import pandas as pd

from load_data import load
from preprocess import preprocess

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CHART = Path("outputs/student_predictions.png")

# Two example students (made-up profiles for the demo)
NEW_STUDENTS = [
    {"name": "Student A", "studytime": 3, "failures": 0, "absences": 2,
     "goout": 2, "higher": "yes", "G1": 13, "G2": 14},
    {"name": "Student B", "studytime": 1, "failures": 2, "absences": 18,
     "goout": 5, "higher": "no", "G1": 8, "G2": 7},
]


def risk_label(p):
    return "LOW risk" if p >= 0.7 else "MEDIUM risk" if p >= 0.4 else "HIGH risk"


if __name__ == "__main__":
    bundle = joblib.load("build/best_model.joblib")
    model, features = bundle["model"], bundle["features"]

    # Start from a typical student (most common value of every column), then
    # overwrite the fields we know - unknown fields get a sensible default.
    template = load().mode().iloc[0]
    rows = []
    for s in NEW_STUDENTS:
        row = template.copy()
        for key, value in s.items():
            if key != "name":
                row[key] = value
        rows.append(row)
    new = pd.DataFrame(rows)

    # Same preprocessing as training, then same column order as training
    X_new, _ = preprocess(new)
    X_new = X_new.reindex(columns=features, fill_value=0)

    proba = model.predict_proba(X_new)[:, 1]          # P(pass)
    print(f"Model: {bundle['name']}\n")
    for s, p in zip(NEW_STUDENTS, proba):
        shown = {k: v for k, v in s.items() if k != "name"}
        print(f"{s['name']}: {shown}")
        print(f"  -> P(pass) = {p:.0%}  |  {risk_label(p)}\n")
    print("Action: HIGH-risk students are flagged for mentoring / extra classes.")

    # ---- Chart: probability of passing, coloured by risk band ----
    fig, ax = plt.subplots(figsize=(8, 2.4), dpi=120)
    names = [s["name"] for s in NEW_STUDENTS][::-1]
    probs = list(proba)[::-1]
    colors = ["#30d158" if p >= 0.7 else "#ff9f0a" if p >= 0.4 else "#ff453a"
              for p in probs]
    ax.barh(names, [1] * len(names), color="#e5e5ea")      # 100% track
    ax.barh(names, probs, color=colors)
    for i, p in enumerate(probs):
        ax.text(min(p + 0.02, 0.9), i, f"{p:.0%}  {risk_label(p)}",
                va="center", fontsize=9)
    ax.axvline(0.4, ls=":", color="#8e8e93"), ax.axvline(0.7, ls=":", color="#8e8e93")
    ax.set_xlim(0, 1), ax.set_title("Predicted probability of passing",
                                    fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"Chart: {CHART}")
