"""
ReelPick - Step 4: The recommend() function
===========================================
Given a movie title, return the most similar movies.
  * Fuzzy title matching - "dark knight" or a small typo still finds
    "The Dark Knight", using difflib from the standard library.
  * Quality filter - skip obscure movies with very few votes, because a
    perfect content match nobody has rated is a poor suggestion.
"""
import difflib
from functools import lru_cache
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CHART = Path("outputs/reelpick_recommendations.png")


@lru_cache(maxsize=1)            # load the data once, reuse on every call
def _data():
    movies = pd.read_pickle("build/movies_clean.pkl")
    nb = np.load("build/neighbours.npz")
    return movies, nb["idx"], nb["score"]


def find_title(query):
    movies, _, _ = _data()
    titles = movies["title"].tolist()
    exact = [t for t in titles if t.lower() == query.lower()]
    if exact:
        return exact[0]
    close = difflib.get_close_matches(query, titles, n=1, cutoff=0.5)
    if close:
        return close[0]
    contains = [t for t in titles if query.lower() in t.lower()]
    return contains[0] if contains else None


def recommend(query, n=5, min_votes=200):
    movies, idx, score = _data()
    title = find_title(query)
    if title is None:
        return None, []
    i = movies.index[movies["title"] == title][0]
    picks = []
    for j, s in zip(idx[i], score[i]):           # already sorted best-first
        m = movies.iloc[j]
        if m["vote_count"] >= min_votes:
            picks.append({"title": m["title"], "year": int(m["year"]),
                          "rating": m["vote_average"], "match": float(s),
                          "genres": ", ".join(m["genre_list"][:3])})
        if len(picks) == n:
            break
    return title, picks


if __name__ == "__main__":
    results = []
    for query in ["The Dark Knight Rises", "avatar", "Toy Strory", "inception"]:
        title, picks = recommend(query)
        note = "" if title.lower() == query.lower() else f"  (matched '{query}')"
        print(f"Because you liked: {title}{note}")
        for k, p in enumerate(picks, 1):
            print(f"  {k}. {p['title']:<38} {p['year']}  "
                  f"rating {p['rating']:.1f}  match {p['match']:.0%}")
        print()
        results.append((title, picks))

    # ---- Chart: match scores for each query ----
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.6), dpi=120)
    for ax, (title, picks) in zip(axes.flat, results):
        names = [p["title"] for p in picks][::-1]
        scores = [p["match"] * 100 for p in picks][::-1]
        ax.barh(names, scores, color="#ff4b4b")
        for i, v in enumerate(scores):
            ax.text(v + 0.5, i, f"{v:.0f}%", va="center", fontsize=8)
        ax.set_xlim(0, 60)
        ax.set_title(f"Because you liked {title}", fontsize=10)
        ax.tick_params(axis="y", labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART, bbox_inches="tight")
    print(f"Chart: {CHART}")
