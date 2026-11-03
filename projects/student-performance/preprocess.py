"""
Student Performance Prediction - Step 2: Preprocess
===================================================
Machine-learning models only understand numbers, so this step:
  1. creates the TARGET  ->  passed = 1 if G3 >= 10, else 0
  2. turns yes/no columns into 1/0
  3. turns two-option columns (e.g. sex F/M) into 1/0
  4. one-hot encodes columns with several options (e.g. mother's job)
  5. removes G3 from the inputs - it is the target itself, so keeping it
     would be target leakage
"""
from pathlib import Path

import pandas as pd

IN, OUT = Path("build/raw.pkl"), Path("build/dataset.pkl")

YES_NO = ["schoolsup", "famsup", "paid", "activities", "nursery", "higher",
          "internet", "romantic"]
TWO_OPTIONS = {"school": "MS", "sex": "M", "address": "U",
               "famsize": "GT3", "Pstatus": "T"}      # value that becomes 1
MULTI_OPTIONS = ["Mjob", "Fjob", "reason", "guardian"]


def preprocess(df):
    df = df.copy()
    y = (df["G3"] >= 10).astype(int)                  # 1 = passed

    for col in YES_NO:
        df[col] = (df[col] == "yes").astype(int)
    for col, one in TWO_OPTIONS.items():
        df[col] = (df[col] == one).astype(int)
    # drop_first avoids a redundant column (if not A, B or C it must be D)
    df = pd.get_dummies(df, columns=MULTI_OPTIONS, drop_first=True, dtype=int)

    X = df.drop(columns=["G3"])                       # no target leakage
    return X, y


if __name__ == "__main__":
    raw = pd.read_pickle(IN)
    X, y = preprocess(raw)
    pd.to_pickle({"X": X, "y": y}, OUT)

    print(f"Columns before encoding: {raw.shape[1]} (incl. target G3)")
    print(f"Feature columns after encoding: {X.shape[1]}")
    print(f"All numeric now: {all(pd.api.types.is_numeric_dtype(t) for t in X.dtypes)}")

    print("\nExample - one-hot encoding of mother's job (Mjob):")
    mjob_cols = [c for c in X.columns if c.startswith("Mjob_")]
    for i in raw.drop_duplicates("Mjob").index:       # one row per job type
        print(f"  {raw.loc[i, 'Mjob']:<9} -> {X.loc[i, mjob_cols].tolist()}")
    print(f"  columns: {mjob_cols}  ('at_home' = all zeros, the dropped one)")

    print(f"\nTarget 'passed': {y.sum()} x 1 (pass), "
          f"{(1 - y).sum()} x 0 (fail)  -> {y.mean():.0%} positive")
    print("Classes are imbalanced (2:1), so we will report F1 and use a "
          "stratified split, not just accuracy.")
    print(f"\nSaved {OUT}")
