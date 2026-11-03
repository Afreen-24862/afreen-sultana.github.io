"""
CityAir AI - Step 1: Load Hyderabad's air-quality data
=======================================================
Source: CPCB daily readings for Hyderabad, from the public Kaggle dataset
"Air Quality Data in India (2015-2020)" (file city_day.csv, Hyderabad rows).

This step only READS and INSPECTS the data - no changes yet. Looking at the
raw data first tells us what cleaning the next step has to do.
"""
from pathlib import Path

import pandas as pd

DATA = Path("data/hyderabad_city_day.csv")
OUT = Path("build/raw.pkl")

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
    print(df["AQI_Bucket"].value_counts().to_string())
    print(f"\nSaved {OUT}")
