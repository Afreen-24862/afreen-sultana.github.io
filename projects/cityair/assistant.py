"""
CityAir AI - Step 5: The LLM assistant
======================================
This is where data science meets the user. For each question we:
  1. build a FACT SHEET from the data (today's AQI, main pollutant, trend,
     and tomorrow's forecast from the step-4 model),
  2. put the fact sheet + the question into a PROMPT with clear rules,
  3. send it to an LLM (Google Gemini) and return a plain-language answer.

Grounding the LLM in our own numbers means it explains Hyderabad's real
data instead of guessing. If no API key is configured, a rule-based
fallback answers from the same fact sheet so the app still works offline.
"""
import json
import os
import urllib.request
from pathlib import Path

import joblib
import pandas as pd

FEATURES = Path("build/features.pkl")
MODEL = Path("build/aqi_model.joblib")

# CPCB national AQI categories (upper limit, label, health message)
CATEGORIES = [
    (50, "Good", "Minimal impact."),
    (100, "Satisfactory", "Minor breathing discomfort for sensitive people."),
    (200, "Moderate", "Discomfort for people with asthma, lung or heart disease."),
    (300, "Poor", "Breathing discomfort for most people on prolonged exposure."),
    (400, "Very Poor", "Respiratory illness on prolonged exposure."),
    (999, "Severe", "Affects healthy people; serious for those with disease."),
]
# 24-hour safe limits (NAAQS India) - used to find the "main culprit"
SAFE_LIMIT = {"PM2.5": 60, "NO2": 80, "SO2": 80, "O3": 100}


def category(aqi):
    return next((label, msg) for limit, label, msg in CATEGORIES if aqi <= limit)


def build_fact_sheet():
    df = pd.read_pickle(FEATURES)
    bundle = joblib.load(MODEL)
    today = df.iloc[-1]                                   # latest day we have
    change = bundle["model"].predict(df[bundle["features"]].iloc[[-1]])[0]
    forecast = round(today["AQI"] + change)
    # Main pollutant = the one closest to (or furthest above) its safe limit
    ratios = {p: today[p] / limit for p, limit in SAFE_LIMIT.items()}
    week_ago = df["AQI"].iloc[-8]
    return {
        "date": f"{df.index[-1]:%d %b %Y}",
        "aqi": round(today["AQI"]),
        "category": category(today["AQI"])[0],
        "health_note": category(today["AQI"])[1],
        "main_pollutant": max(ratios, key=ratios.get),
        "pm25": round(today["PM2.5"], 1),
        "trend_7d": "improving" if today["AQI"] < week_ago else "worsening",
        "forecast_tomorrow": forecast,
        "forecast_category": category(forecast)[0],
        "forecast_error": f"+/- {bundle['mae']:.0f} AQI points",
        "season": today["season"],
    }


PROMPT = """You are CityAir, an assistant that explains Hyderabad's air quality
to residents in simple, friendly language.
Rules: use ONLY the facts below; give one practical action; under 80 words;
say it is general information, not medical advice, if health is mentioned.

FACTS:
{facts}

QUESTION: {question}"""


def ask_gemini(prompt):
    """Call Google Gemini's REST API. Returns None if no key is set."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={key}")
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0.3}}).encode()
    req = urllib.request.Request(url, body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def rule_based_answer(facts, question):
    """Offline fallback: answers from the same fact sheet, no LLM needed."""
    q = question.lower()
    head = (f"On {facts['date']} Hyderabad's AQI is {facts['aqi']} "
            f"({facts['category']}).")
    if any(w in q for w in ("run", "jog", "exercise", "walk", "outside")):
        ok = facts["aqi"] <= 100
        tip = ("Good time to exercise outdoors." if ok else
               "Prefer indoor exercise or go early morning.")
        return f"{head} {tip} Tomorrow looks {facts['forecast_category']}."
    if "tomorrow" in q or "forecast" in q:
        return (f"{head} Tomorrow's forecast is about "
                f"{facts['forecast_tomorrow']} ({facts['forecast_category']}, "
                f"{facts['forecast_error']}). The trend is "
                f"{facts['trend_7d']} over the last week.")
    if any(w in q for w in ("reduce", "help", "do")):
        return (f"{head} The main pollutant today is {facts['main_pollutant']}, "
                f"mostly from traffic and dust. Use the metro or carpool, "
                f"avoid burning waste and keep vehicles serviced.")
    return f"{head} {facts['health_note']} (General info, not medical advice.)"


def answer(question, facts):
    prompt = PROMPT.format(facts=json.dumps(facts, indent=1), question=question)
    reply = ask_gemini(prompt)
    if reply:
        return "gemini", prompt, reply
    return "offline fallback", prompt, rule_based_answer(facts, question)


if __name__ == "__main__":
    facts = build_fact_sheet()
    print("FACT SHEET built from the data + forecast model:")
    print(json.dumps(facts, indent=1))
    actual = pd.read_pickle(FEATURES)["AQI_next"].iloc[-1]
    print(f"Check: forecast {facts['forecast_tomorrow']} vs actual AQI "
          f"next day {actual:.0f}")

    questions = ["Is it safe to go for a run this evening?",
                 "What will the air be like tomorrow?",
                 "What can I do to help reduce pollution?"]
    for i, q in enumerate(questions):
        mode, prompt, reply = answer(q, facts)
        if i == 0:
            print("\nPROMPT sent to the LLM (shortened):")
            print(prompt[:330] + " ...")
        print(f"\nQ: {q}\nA [{mode}]: {reply}")
