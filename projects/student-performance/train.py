"""
Student Performance Prediction - Step 4: Train and compare models
=================================================================
We compare 3 classic classifiers in 2 scenarios:

  Scenario A - "Early warning": WITHOUT term grades G1/G2. Uses only
               background and habits, so it works at the START of the year,
               when a teacher can still help.
  Scenario B - "With term grades": includes G1/G2. More accurate, but only
               available later in the year.

Evaluation method:
  * a "baseline" that always predicts PASS - any model must beat it
  * stratified 80/20 train/test split - keeps the 67/33 pass/fail ratio
  * 5-fold cross-validation (macro F1) on the training part picks the model
  * class_weight="balanced" - failing students are the minority, but they
    are exactly who we want to find, so their mistakes count more
  * "at-risk recall" = share of failing students the model catches
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

OUT = Path("build/best_model.joblib")


def candidate_models():
    return {
        # Always says "pass" - the score to beat
        "Baseline (always pass)": DummyClassifier(strategy="most_frequent"),
        # Scaling matters for logistic regression (gradient-based optimiser)
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced")),
        # A shallow tree is easy to explain as if/else rules
        "Decision Tree": DecisionTreeClassifier(
            max_depth=4, class_weight="balanced", random_state=42),
        # Many trees on random subsets -> less overfitting than one tree
        "Random Forest": RandomForestClassifier(
            n_estimators=300, min_samples_leaf=2, class_weight="balanced",
            random_state=42, n_jobs=-1),
    }


def run_scenario(X, y, title):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    rows, fitted = [], {}
    for name, model in candidate_models().items():
        cv = cross_val_score(model, X_train, y_train, cv=5, scoring="f1_macro")
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rows.append({
            "model": name,
            "CV macro-F1": cv.mean(),
            "Test acc": accuracy_score(y_test, pred),
            "Balanced acc": balanced_accuracy_score(y_test, pred),
            "At-risk recall": recall_score(y_test, pred, pos_label=0),
        })
        fitted[name] = model
    table = pd.DataFrame(rows).set_index("model").round(3)
    print(f"\n{title}  ({X.shape[1]} features, train {len(X_train)} / "
          f"test {len(X_test)})")
    print(table.to_string())
    best = table["CV macro-F1"].idxmax()     # choose by CV, never by test
    print(f"-> chosen by cross-validation: {best}")
    return best, fitted[best], (X_test, y_test), table


if __name__ == "__main__":
    data = pd.read_pickle("build/dataset.pkl")
    X, y = data["X"], data["y"]

    _, _, _, early = run_scenario(X.drop(columns=["G1", "G2"]), y,
                                  "Scenario A - early warning (no G1/G2)")
    best, model, test_set, late = run_scenario(
        X, y, "Scenario B - with term grades (G1, G2)")

    print(f"\nInsight: without grades the best model catches "
          f"{early['At-risk recall'].max():.0%} of failing students; "
          f"with term grades it catches {late.loc[best, 'At-risk recall']:.0%}.")
    joblib.dump({"model": model, "name": best, "features": list(X.columns),
                 "test": test_set}, OUT)
    print(f"Saved {best} (scenario B) to {OUT}")
