# Project source code

The code behind the **Code walkthrough** section of the portfolio. Each project is split into small modules that run in order; the website shows every module's source, a plain-English explanation and the output it printed.

| Project | Folder | Data | Run |
|---|---|---|---|
| AIRA (final-year project) | [`aira-lite/`](aira-lite) | Research-paper PDFs | FastAPI + React app — see folder README |
| CityAir AI | [`cityair/`](cityair) | CPCB daily readings, Hyderabad 2015–2020 | `load_data → clean_features → eda → train_model → assistant` |
| Student Performance | [`student-performance/`](student-performance) | UCI Student Performance (395 students) | `load_data → preprocess → eda → train → evaluate → predict` |
| ReelPick | [`reelpick/`](reelpick) | TMDB 5000 movies + credits | `load_data → preprocess → vectorize → recommend → app` |
| Resume Screening | [`resume-screening/`](resume-screening) | Job description + 4 sample resumes | `extract_text → preprocess → skills → matcher → rank` |

## Run a project

```bash
cd projects/cityair
pip install -r requirements.txt
python load_data.py && python clean_features.py && python eda.py && python train_model.py && python assistant.py
```

Each step saves its result in `build/` for the next step, and charts in `outputs/`.

## Refresh the website

From the repository root:

```bash
python tools/build_codelab.py
```

This runs every module again, captures the printed output, timings and charts, and writes `js/codelab-data.js` (plus charts in `assets/codelab/`). The website itself stays static.
