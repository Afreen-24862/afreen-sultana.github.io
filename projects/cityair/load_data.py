"""
CityAir AI - Step 1: Load Hyderabad's air-quality data
=======================================================
Source: CPCB daily readings for Hyderabad, from the public Kaggle dataset
"Air Quality Data in India (2015-2020)" (file city_day.csv, Hyderabad rows).

This step only READS and INSPECTS the data - no changes yet. Looking at the
raw data first tells us what cleaning the next step has to do.
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")                     # draw charts without a screen
import matplotlib.pyplot as plt  # noqa: E402

DATA = Path("data/hyderabad_city_day.csv")
OUT = Path("build/raw.pkl")
CHART = Path("outputs/cityair_data_profile.png")
CATEGORY_ORDER = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor",
                  "Severe"]
CATEGORY_COLOR = ["#30d158", "#a3d977", "#ffd60a", "#ff9f0a", "#ff453a",
                  "#a2123b"]

# The pollutants CPCB measures (all in micrograms per cubic metre, CO in mg/m3)
POLLUTANTS = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3",
              "Benzene", "Toluene", "Xylene"]


def load(path=DATA):
    # parse_dates turns the text "2015-01-04" into a real date, so we can
    # sort, filter by year and resample by month later
    df = pd.read_csv(path, parse_dates=["Date"])
    return df.sort_values("Date").reset_index(drop=True)


if __name__ == "__main__":
    df = load()
    OUT.parent.mkdir(exist_ok=True)
    df.to_pickle(OUT)                      # hand the data to the next step

    # 1) How big is it and what period does it cover?
    print(f"Rows: {len(df):,}   Columns: {df.shape[1]}")
    print(f"City: {df['City'].unique()[0]}")
    print(f"Period: {df['Date'].min():%d %b %Y} -> {df['Date'].max():%d %b %Y}")

    # 2) Are any days missing from the calendar?
    full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    print(f"Calendar days in period: {len(full_range):,} "
          f"(missing dates: {len(full_range) - len(df)})")

    # 3) How much of each column is empty? Decides what we can trust.
    missing = df[POLLUTANTS + ["AQI"]].isna().mean().mul(100).round(1)
    print("\nMissing values (%):")
    for col, pct in missing.sort_values(ascending=False).items():
        bar = "#" * int(pct / 2)
        print(f"  {col:<8} {pct:5.1f}%  {bar}")

    # 4) What does a typical day look like?
    print("\nAQI summary:")
    print(df["AQI"].describe().round(1).to_string())

    # 5) How often is the air Good / Moderate / Poor ...?
    print("\nDays per AQI category:")
    counts = df["AQI_Bucket"].value_counts().reindex(CATEGORY_ORDER).fillna(0)
    print(counts.astype(int).to_string())

    # ---- Chart: data quality (left) and how often each category occurs ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.6), dpi=120)
    m = missing.sort_values()
    ax1.barh(m.index, m.values, color=["#ff9f0a" if v > 10 else "#0071e3"
                                       for v in m.values])
    ax1.set_title("Missing values per column (%)", fontsize=10)
    ax2.bar(counts.index, counts.values, color=CATEGORY_COLOR)
    ax2.set_title("Days per AQI category (2015-2020)", fontsize=10)
    ax2.tick_params(axis="x", labelsize=8, rotation=20)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    CHART.parent.mkdir(exist_ok=True)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nSaved {OUT} | Chart: {CHART}")
