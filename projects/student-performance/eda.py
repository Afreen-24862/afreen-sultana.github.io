"""
Student Performance Prediction - Step 3: Exploratory data analysis
==================================================================
Which factors are linked to passing? EDA gives us hypotheses to check and
helps explain the model later. Note: correlation is not causation - these
are associations in this dataset only.
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CHART = Path("outputs/student_eda.png")

if __name__ == "__main__":
    raw = pd.read_pickle("build/raw.pkl")
    data = pd.read_pickle("build/dataset.pkl")
    X, y = data["X"], data["y"]

    # 1) Correlation of every encoded feature with the pass/fail target
    corr = X.corrwith(y).sort_values()
    print("Strongest links with passing (correlation, -1 to +1):")
    for name, v in pd.concat([corr.tail(5)[::-1], corr.head(5)]).items():
        bar = ("+" if v > 0 else "-") * int(abs(v) * 30)
        print(f"  {name:<15} {v:+.2f}  {bar}")

    # 2) Pass rate by number of past class failures
    by_fail = (raw.assign(passed=y).groupby("failures")["passed"]
               .agg(["mean", "count"]))
    print("\nPass rate by past failures:")
    for f, row in by_fail.iterrows():
        print(f"  {f} failures: {row['mean']:.0%} pass  (n={int(row['count'])})")

    # 3) Pass rate by weekly study time (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)
    labels = {1: "<2h", 2: "2-5h", 3: "5-10h", 4: ">10h"}
    by_study = raw.assign(passed=y).groupby("studytime")["passed"].mean()
    print("\nPass rate by weekly study time:")
    for s, v in by_study.items():
        print(f"  {labels[s]:<6} {v:.0%}")

    # 4) How well do earlier term grades track the final grade?
    print(f"\nCorrelation of G1 with G3: {raw['G1'].corr(raw['G3']):.2f} | "
          f"G2 with G3: {raw['G2'].corr(raw['G3']):.2f}")
    print("-> Term grades are very strong predictors; step 4 tests the model "
          "with AND without them.")

    # ---- Chart ----
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), dpi=120)
    axes[0].bar(by_fail.index.astype(str), by_fail["mean"] * 100,
                color=["#30d158", "#ffd60a", "#ff9f0a", "#ff453a"])
    axes[0].set_title("Pass rate % by past failures", fontsize=10)
    axes[1].bar([labels[s] for s in by_study.index], by_study.values * 100,
                color="#0071e3")
    axes[1].set_title("Pass rate % by study time / week", fontsize=10)
    colors = ["#30d158" if p else "#ff453a" for p in y]
    axes[2].scatter(raw["G2"], raw["G3"], c=colors, s=12, alpha=0.7)
    axes[2].set_xlabel("G2 (second term)"), axes[2].set_ylabel("G3 (final)")
    axes[2].set_title("G2 vs final grade (green = pass)", fontsize=10)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    CHART.parent.mkdir(exist_ok=True)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nChart: {CHART}")
