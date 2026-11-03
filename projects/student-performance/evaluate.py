"""
Student Performance Prediction - Step 5: Evaluate the chosen model
==================================================================
A single accuracy number hides WHICH mistakes the model makes. Here we look at:
  * the confusion matrix - how many pass/fail students were mixed up
  * precision / recall per class
  * feature importance - which inputs the Random Forest relies on, so a
    teacher can understand (and trust) the prediction
"""
from pathlib import Path

import joblib
import matplotlib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CHART = Path("outputs/student_evaluation.png")

if __name__ == "__main__":
    bundle = joblib.load("build/best_model.joblib")
    model, (X_test, y_test) = bundle["model"], bundle["test"]
    pred = model.predict(X_test)

    print(f"Model: {bundle['name']} | test students: {len(y_test)}\n")
    print(classification_report(y_test, pred, target_names=["fail", "pass"],
                                digits=2))

    cm = confusion_matrix(y_test, pred)        # rows = truth, cols = predicted
    (tn, fp), (fn, tp) = cm
    print("Confusion matrix:")
    print("                 predicted fail  predicted pass")
    print(f"  actually fail  {tn:^14}  {fp:^14}")
    print(f"  actually pass  {fn:^14}  {tp:^14}")
    print(f"-> {fp} failing student(s) were missed (predicted pass) - "
          f"the costly mistake for an early-warning tool.")

    # Feature importance: how much each input reduces impurity across trees
    importance = (pd.Series(model.feature_importances_,
                            index=bundle["features"])
                  .sort_values(ascending=False))
    print("\nTop 8 features:")
    for name, v in importance.head(8).items():
        print(f"  {name:<10} {v:.3f}  {'#' * int(v * 80)}")

    # ---- Chart: confusion matrix + top-10 importance ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=120,
                                   gridspec_kw={"width_ratios": [1, 1.5]})
    ax1.imshow(cm, cmap="Blues")
    for (i, j), v in pd.DataFrame(cm).stack().items():
        ax1.text(j, i, v, ha="center", va="center", fontsize=14,
                 color="white" if v > cm.max() / 2 else "#1d1d1f")
    ax1.set_xticks([0, 1], ["fail", "pass"]), ax1.set_yticks([0, 1], ["fail", "pass"])
    ax1.set_xlabel("Predicted"), ax1.set_ylabel("Actual")
    ax1.set_title("Confusion matrix (test set)", fontsize=10)
    top = importance.head(10)[::-1]
    ax2.barh(top.index, top.values, color="#0071e3")
    ax2.set_title("Top 10 feature importances", fontsize=10)
    ax2.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nChart: {CHART}")
