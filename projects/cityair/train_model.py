"""
CityAir AI - Step 4: Train a model to forecast tomorrow's AQI
=============================================================
Why a forecast? The assistant should not only say "the air is bad today"
but warn people BEFORE a bad day, so they can plan.

Two key decisions (both are good interview talking points):

1. TIME-BASED split, not a random split.
   train = 2015-2019, test = 2020. A random split would let the model peek at
   days right next to the test days, which inflates the score and could never
   happen in real life (we cannot train on the future).

2. Predict the CHANGE, not the level.
   Tomorrow's AQI is usually close to today's, so the model learns
   "how much will it go up or down?" and we add that to today's AQI.
   This copes better with 2020, when lockdown pushed AQI below normal levels.
"""
from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from clean_features import MODEL_FEATURES, TARGET

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

IN = Path("build/features.pkl")
MODEL_OUT = Path("build/aqi_model.joblib")
CHART = Path("outputs/cityair_forecast.png")


def scores(y_true, y_pred):
    """MAE = average error in AQI points; R2 = share of variation explained."""
    return {"MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "R2": r2_score(y_true, y_pred)}


if __name__ == "__main__":
    df = pd.read_pickle(IN)
    train, test = df[df.index.year <= 2019], df[df.index.year == 2020]
    X_train, X_test = train[MODEL_FEATURES], test[MODEL_FEATURES]
    y_test = test[TARGET]                          # true AQI of the next day
    change_train = train[TARGET] - train["AQI"]    # what the model learns
    print(f"Train: {len(train):,} days (2015-2019) | "
          f"Test: {len(test)} days (2020)\n")

    models = {
        # Linear Regression - simple, fast, easy to explain
        "Linear Regression": LinearRegression(),
        # Random Forest - many decision trees averaged together; captures
        # non-linear effects such as "winter + rising PM2.5 = big jump"
        "Random Forest": RandomForestRegressor(
            n_estimators=300, min_samples_leaf=5, random_state=42, n_jobs=-1),
    }

    # Baseline: "tomorrow = today". A real model must beat this to be useful.
    results = {"Baseline (tomorrow = today)": scores(y_test, test["AQI"])}
    forecasts = {}
    for name, model in models.items():
        model.fit(X_train, change_train)
        forecasts[name] = test["AQI"] + model.predict(X_test)  # level = today + change
        results[name] = scores(y_test, forecasts[name])

    table = pd.DataFrame(results).T.round(2)
    print("Next-day AQI forecast on unseen 2020 data:")
    print(table.to_string())

    best_name = table.drop(index=table.index[0])["MAE"].idxmin()
    gain = 1 - table.loc[best_name, "MAE"] / table.iloc[0]["MAE"]
    print(f"\nBest model: {best_name} -> {gain:.0%} lower error than baseline")

    # Which inputs does the forest rely on most?
    forest = models["Random Forest"]
    importance = pd.Series(forest.feature_importances_, index=MODEL_FEATURES)
    print("\nTop features (Random Forest importance):")
    for name, v in importance.sort_values(ascending=False).head(5).items():
        print(f"  {name:<11} {v:.2f}  {'#' * int(v * 60)}")

    # Save everything the assistant (step 5) needs to make a forecast
    joblib.dump({"model": models[best_name], "name": best_name,
                 "features": MODEL_FEATURES, "mae": table.loc[best_name, "MAE"]},
                MODEL_OUT)

    # Chart: actual vs predicted AQI across 2020
    fig, ax = plt.subplots(figsize=(9, 3.6), dpi=120)
    ax.plot(y_test.index, y_test.values, color="#8e8e93", lw=1.4,
            label="Actual AQI (next day)")
    ax.plot(y_test.index, forecasts[best_name].values, color="#0071e3",
            lw=1.6, label=f"Forecast - {best_name}")
    ax.set_title(f"2020 forecast vs reality (MAE "
                 f"{table.loc[best_name, 'MAE']:.1f} AQI points)", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nSaved {MODEL_OUT} | Chart: {CHART}")
