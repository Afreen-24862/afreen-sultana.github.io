"""
ReelPick - Step 2: Build one "tags" text per movie
==================================================
Content-based filtering compares movies by their CONTENT. We describe each
movie with a bag of words ("tags") made of:
    overview words + genres + keywords + top-3 cast + director

Trick: multi-word names are joined into one token ("Sam Worthington" ->
"samworthington"). Otherwise every "Sam" or "Johnson" would look related.
"""
import json
from pathlib import Path

import pandas as pd

IN, OUT = Path("build/movies_raw.pkl"), Path("build/movies_clean.pkl")


def names(json_text, limit=None):
    """'[{"name": "Action"}, {"name": "Drama"}]' -> ['Action', 'Drama']"""
    items = [d["name"] for d in json.loads(json_text)]
    return items[:limit] if limit else items


def director(crew_json):
    return [d["name"] for d in json.loads(crew_json) if d["job"] == "Director"]


def squash(tokens):
    """Remove spaces inside names so each name is one unique word."""
    return [t.replace(" ", "").lower() for t in tokens]


def build_tags(df):
    df = df.dropna(subset=["overview"]).copy()        # 3 movies have no text
    df["genre_list"] = df["genres"].apply(names)
    df["tags"] = (
        df["overview"].str.lower().str.split()
        + df["genre_list"].apply(squash)
        + df["keywords"].apply(names).apply(squash)
        + df["cast"].apply(names, limit=3).apply(squash)      # top-3 actors
        + df["crew"].apply(director).apply(squash)
    ).apply(" ".join)
    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    keep = ["id", "title", "year", "genre_list", "vote_average",
            "vote_count", "tags"]
    return df[keep].reset_index(drop=True)


if __name__ == "__main__":
    clean = build_tags(pd.read_pickle(IN))
    clean.to_pickle(OUT)
    print(f"Movies with tags: {len(clean):,}")
    lengths = clean["tags"].str.split().str.len()
    print(f"Tag length (words): median {lengths.median():.0f}, "
          f"max {lengths.max()}")

    row = clean[clean["title"] == "The Dark Knight Rises"].iloc[0]
    print(f"\nExample - {row['title']} ({row['year']:.0f}):")
    print(f"  genres: {row['genre_list']}")
    tags = row["tags"].split()
    print(f"  tags ({len(tags)} words): {' '.join(tags[:18])} ...")
    print(f"  ... {' '.join(tags[-12:])}")
    print(f"\nSaved {OUT}")
