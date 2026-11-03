"""
CityAir AI - Step 3: Exploratory data analysis (EDA)
====================================================
Before training any model we look for the patterns the assistant should
explain to residents:
  1. Is Hyderabad's air getting better or worse over the years?
  2. Which season is the most polluted?
  3. Which pollutant drives the AQI?
  4. A natural experiment: what happened during the 2020 lockdown?
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")                     # draw charts without a screen
import matplotlib.pyplot as plt  # noqa: E402

IN = Path("build/features.pkl")
CHART = Path("outputs/cityair_eda.png")
SEASONS = ["Winter", "Summer", "Monsoon", "Post-monsoon"]

if __name__ == "__main__":
    df = pd.read_pickle(IN)

    # 1) Yearly trend - mean AQI per calendar year
    yearly = df["AQI"].groupby(df.index.year).mean().round(1)
    print("Mean AQI by year:")
    for year, v in yearly.items():
        print(f"  {year}  {v:6.1f}  {'#' * int(v / 5)}")

    # 2) Seasonal pattern - group by the season we engineered in step 2
    seasonal = df.groupby("season")["AQI"].mean().reindex(SEASONS).round(1)
    print("\nMean AQI by season:")
    print(seasonal.to_string())
    print(f"-> Worst: {seasonal.idxmax()} | Cleanest: {seasonal.idxmin()} "
          f"(rain washes particles out of the air)")

    # 3) Which pollutant moves with AQI the most? (Pearson correlation)
    corr = (df[["PM2.5", "NO2", "CO", "SO2", "O3"]]
            .corrwith(df["AQI"]).sort_values(ascending=False).round(2))
    print("\nCorrelation with AQI:")
    print(corr.to_string())

    # 4) Lockdown: same weeks (Apr-May) in 2019 vs 2020
    def apr_may(year):
        return df.loc[f"{year}-04-01":f"{year}-05-31", ["AQI", "PM2.5", "NO2"]]
    before, during = apr_may(2019).mean(), apr_may(2020).mean()
    change = ((during - before) / before * 100).round(1)
    print("\nLockdown effect (Apr-May 2020 vs Apr-May 2019):")
    for col in change.index:
        print(f"  {col:<6} {before[col]:6.1f} -> {during[col]:6.1f}  "
              f"({change[col]:+.1f}%)")

    # ---- Chart: monthly trend + season bars + lockdown comparison ----
    monthly = df["AQI"].resample("MS").mean()
    fig = plt.figure(figsize=(9, 5.4), dpi=120)
    grid = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.45)
    ax1 = fig.add_subplot(grid[0, :])
    ax1.plot(monthly.index, monthly.values, color="#0071e3", lw=1.8)
    ax1.fill_between(monthly.index, monthly.values, alpha=0.12,
                     color="#0071e3")
    ax1.axhline(100, ls="--", lw=0.8, color="#ff9f0a")
    ax1.text(monthly.index[1], 104, "AQI 100 (Moderate limit)", fontsize=7,
             color="#c77700")
    ax1.set_title("Hyderabad monthly mean AQI, 2015-2020", fontsize=10)

    ax2 = fig.add_subplot(grid[1, 0])
    colors = ["#5e5ce6", "#ff9f0a", "#30d158", "#bf5af2"]
    ax2.bar(seasonal.index, seasonal.values, color=colors)
    ax2.set_title("Mean AQI by season", fontsize=10)
    ax2.tick_params(axis="x", labelsize=7)

    ax3 = fig.add_subplot(grid[1, 1])
    x = range(len(change))
    ax3.bar([i - 0.2 for i in x], before.values, 0.4, label="Apr-May 2019",
            color="#8e8e93")
    ax3.bar([i + 0.2 for i in x], during.values, 0.4, label="Apr-May 2020",
            color="#30d158")
    ax3.set_xticks(list(x), change.index)
    ax3.legend(fontsize=7, frameon=False)
    ax3.set_title("Lockdown: before vs during", fontsize=10)
    for ax in (ax1, ax2, ax3):
        ax.spines[["top", "right"]].set_visible(False)
    CHART.parent.mkdir(exist_ok=True)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nChart: {CHART}")
