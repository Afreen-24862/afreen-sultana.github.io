# CityAir AI — Hyderabad air quality

Forecasts tomorrow's AQI for Hyderabad and explains the air in plain language with an LLM assistant grounded in the data.

| Step | File | What it does |
|---|---|---|
| 1 | `load_data.py` | Load and profile CPCB daily readings (2015–2020) |
| 2 | `clean_features.py` | Fill short gaps, cap outliers, lag/rolling/season features, next-day target |
| 3 | `eda.py` | Yearly trend, seasons, main pollutant, 2020 lockdown effect |
| 4 | `train_model.py` | Linear Regression vs Random Forest vs "tomorrow = today" baseline, time-based split |
| 5 | `assistant.py` | Fact sheet + grounded prompt → Gemini (rule-based fallback without an API key) |

Data: Hyderabad rows of `city_day.csv` from the Kaggle dataset *Air Quality Data in India (2015–2020)* (source: CPCB).
Set `GEMINI_API_KEY` (and optionally `GEMINI_MODEL`) to use the LLM; never commit the key.
