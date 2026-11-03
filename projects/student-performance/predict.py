"""
Student Performance Prediction - Step 6: Predict for new students
=================================================================
How the model is used in practice: a teacher enters a student's details,
we apply EXACTLY the same preprocessing as in training, and the model
returns the probability of passing plus a risk label.

Re-using preprocess() from step 2 is important - if training and prediction
encoded data differently, the model would silently give wrong answers.
"""
import joblib
import pandas as pd

from load_data import load
from preprocess import preprocess

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
