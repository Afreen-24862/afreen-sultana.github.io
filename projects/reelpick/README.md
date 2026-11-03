# ReelPick — movie recommender

Content-based recommendations from overview, genres, keywords, cast and director.

| Step | File | What it does |
|---|---|---|
| 1 | `load_data.py` | Join TMDB movies + credits |
| 2 | `preprocess.py` | Parse JSON columns, build one "tags" text per movie |
| 3 | `vectorize.py` | CountVectorizer + cosine similarity, keep top-30 neighbours |
| 4 | `recommend.py` | Fuzzy title match + vote filter → top-N similar movies |
| 5 | `app.py` | Streamlit UI — `streamlit run app.py` |

Data: TMDB 5000 Movies (Kaggle), trimmed to the columns used and gzipped.
