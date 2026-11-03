"""
ReelPick - Step 1: Load the movie data
======================================
Dataset: TMDB 5000 Movies (Kaggle) - two files joined on the movie id:
  * movies  -> title, overview, genres, keywords, rating, votes ...
  * credits -> cast and crew
Genres, keywords, cast and crew are stored as JSON text, e.g.
  '[{"name": "Action"}, {"name": "Adventure"}]'  - parsed in step 2.
"""
from pathlib import Path

import pandas as pd

OUT = Path("build/movies_raw.pkl")


def load():
    movies = pd.read_csv("data/tmdb_5000_movies.csv.gz")
    credits = pd.read_csv("data/tmdb_5000_credits.csv.gz")
    # Join the two tables: one row per movie with all information
    merged = movies.merge(credits.drop(columns="title"),
                          left_on="id", right_on="movie_id")
    return merged.drop(columns="movie_id")


if __name__ == "__main__":
    df = load()
    OUT.parent.mkdir(exist_ok=True)
    df.to_pickle(OUT)

    print(f"Movies: {len(df):,}   Columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns)}")
    years = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    print(f"Release years: {int(years.min())} - {int(years.max())}")
    print(f"Missing overview: {df['overview'].isna().sum()} movies")
    print(f"Median votes per movie: {df['vote_count'].median():.0f}")

    print("\nOne raw row (JSON columns before parsing):")
    row = df[df["title"] == "Avatar"].iloc[0]
    for col in ["title", "genres", "keywords", "cast", "vote_average"]:
        print(f"  {col:<13} {str(row[col])[:95]}")
    print(f"\nSaved {OUT}")
