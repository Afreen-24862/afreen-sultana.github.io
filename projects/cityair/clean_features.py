"""
CityAir AI - Step 2: Clean the data and engineer features
=========================================================
Goal: a tidy daily table where every row can answer
"given today's air, what will tomorrow's AQI be?"

Cleaning decisions:
  * Short sensor gaps (<= 3 days) are filled by time interpolation, because
    air quality changes smoothly from one day to the next.
  * Longer gaps are NOT invented - those rows are dropped instead.
  * Extreme spikes are capped (winsorised) at the 99.5th percentile so one
    festival-night reading cannot dominate the model.
"""
from pathlib import Path

import pandas as pd

IN, OUT = Path("build/raw.pkl"), Path("build/features.pkl")
POLLUTANTS = ["PM2.5", "PM10", "NO2", "NOx", "CO", "SO2", "O3", "NH3"]

# Columns the model will use. PM10 and NH3 are ~18% empty, so the model does
# not depend on them - otherwise we would throw away hundreds of good days.
MODEL_FEATURES = ["AQI", "PM2.5", "NO2", "CO", "SO2", "O3", "month", "dayofweek",
                  "AQI_lag1", "AQI_lag2", "AQI_lag7", "PM2.5_lag1",
                  "AQI_roll7"]
TARGET = "AQI_next"

# Indian Meteorological Department seasons - pollution follows them closely
SEASON = {12: "Winter", 1: "Winter", 2: "Winter",
          3: "Summer", 4: "Summer", 5: "Summer",
          6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
          10: "Post-monsoon", 11: "Post-monsoon"}


def clean(df):
    df = df.set_index("Date")[POLLUTANTS + ["AQI"]]
    # Fill only short gaps; limit=3 stops us inventing long stretches of data
    filled = df.interpolate(method="time", limit=3, limit_area="inside")
    # Cap extreme outliers at the 99.5th percentile of each column
    capped = filled.clip(upper=filled.quantile(0.995), axis=1)
    return capped


def add_features(df):
    out = df.copy()
    # Calendar features: pollution has strong seasonal and weekly patterns
    out["month"] = out.index.month
    out["dayofweek"] = out.index.dayofweek
    out["season"] = out["month"].map(SEASON)
    # Lag features: yesterday's and last week's AQI are the best predictors
    for lag in (1, 2, 7):
        out[f"AQI_lag{lag}"] = out["AQI"].shift(lag)
    out["PM2.5_lag1"] = out["PM2.5"].shift(1)
    # Rolling mean smooths day-to-day noise into a weekly trend
    out["AQI_roll7"] = out["AQI"].rolling(7).mean()
    # TARGET: tomorrow's AQI (shift -1 moves tomorrow's value onto today)
    out["AQI_next"] = out["AQI"].shift(-1)
    # keep rows where everything the model needs is present
    return out.dropna(subset=MODEL_FEATURES + ["AQI", TARGET])


if __name__ == "__main__":
    raw = pd.read_pickle(IN)
    cleaned = clean(raw)
    gaps_before = int(raw[POLLUTANTS + ["AQI"]].isna().sum().sum())
    gaps_after = int(cleaned.isna().sum().sum())
    print(f"Missing cells: {gaps_before:,} before -> {gaps_after:,} after "
          f"filling short gaps (<= 3 days)")

    cap = raw["AQI"].quantile(0.995)
    print(f"AQI capped at 99.5th percentile = {cap:.0f} "
          f"({int((raw['AQI'] > cap).sum())} extreme days affected)")

    feats = add_features(cleaned)
    feats.to_pickle(OUT)
    print(f"Rows ready for modelling: {len(feats):,} of {len(raw):,} "
          f"({len(raw) - len(feats)} dropped: long gaps or no target)")

    new_cols = [c for c in feats.columns if c not in POLLUTANTS + ["AQI"]]
    print(f"\nEngineered features ({len(new_cols)}): {', '.join(new_cols)}")
    print("\nSample rows:")
    show = ["AQI", "AQI_lag1", "AQI_lag7", "AQI_roll7", "season", "AQI_next"]
    print(feats[show].tail(4).round(1).to_string())
    print(f"\nSaved {OUT}")
