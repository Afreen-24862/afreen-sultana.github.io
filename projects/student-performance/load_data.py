"""
Student Performance Prediction - Step 1: Load and understand the data
=====================================================================
Dataset: UCI "Student Performance" (Cortez & Silva, 2008) - 395 students in
a Portuguese secondary-school maths course, 33 columns: demographics,
family background, study habits and the three term grades G1, G2, G3
(each out of 20).

Question we answer: can we predict, early, whether a student will PASS
the final exam (G3 >= 10 out of 20)?
"""
from pathlib import Path

import pandas as pd

DATA = Path("data/student-mat.csv")
OUT = Path("build/raw.pkl")


def load(path=DATA):
    # The file uses ";" as the separator (European CSV style), not ","
    return pd.read_csv(path, sep=";")


if __name__ == "__main__":
    df = load()
    OUT.parent.mkdir(exist_ok=True)
    df.to_pickle(OUT)

    print(f"Shape: {df.shape[0]} students x {df.shape[1]} columns")
    numeric = df.select_dtypes("number").columns
    text = df.select_dtypes(exclude="number").columns
    print(f"Numeric columns ({len(numeric)}): {', '.join(numeric[:10])} ...")
    print(f"Text/categorical ({len(text)}): {', '.join(text[:10])} ...")
    print(f"Missing values: {int(df.isna().sum().sum())}")

    # The target: final grade G3 (0-20). Pass mark is 10.
    print("\nFinal grade G3 distribution:")
    print(df["G3"].describe().round(2).to_string())
    passed = (df["G3"] >= 10)
    print(f"\nPassed (G3 >= 10): {passed.sum()} students ({passed.mean():.0%})")
    print(f"Failed (G3 <  10): {(~passed).sum()} students ({1 - passed.mean():.0%})")
    zeros = (df["G3"] == 0).sum()
    print(f"Note: {zeros} students scored 0 - most likely they did not sit "
          f"the final exam.")

    print("\nFirst 3 rows (selected columns):")
    cols = ["sex", "age", "studytime", "failures", "absences", "G1", "G2", "G3"]
    print(df[cols].head(3).to_string())
    print(f"\nSaved {OUT}")
