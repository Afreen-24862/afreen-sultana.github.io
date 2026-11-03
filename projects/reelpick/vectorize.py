"""
ReelPick - Step 3: Turn tags into vectors and compare every pair of movies
==========================================================================
1. CountVectorizer: each movie becomes a vector of word counts over the
   5,000 most frequent words (English stop-words like "the" removed).
2. Cosine similarity: the angle between two vectors. 1.0 = same words in
   the same proportions, 0.0 = nothing in common. Cosine ignores length, so
   a long overview does not automatically look "more similar".
3. We keep only each movie's top-30 neighbours - the full 4,800 x 4,800
   matrix is ~92 MB (float32), the top-30 table is about 0.5 MB.
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

IN, OUT = Path("build/movies_clean.pkl"), Path("build/neighbours.npz")
TOP_K = 30

if __name__ == "__main__":
    movies = pd.read_pickle(IN)
    vectorizer = CountVectorizer(max_features=5000, stop_words="english")
    vectors = vectorizer.fit_transform(movies["tags"])   # sparse matrix
    density = vectors.nnz / (vectors.shape[0] * vectors.shape[1])
    print(f"Vector matrix: {vectors.shape[0]:,} movies x "
          f"{vectors.shape[1]:,} words (only {density:.2%} non-zero)")

    t0 = time.perf_counter()
    sim = cosine_similarity(vectors).astype("float32")  # every pair at once
    print(f"Similarity matrix: {sim.shape[0]:,} x {sim.shape[1]:,} "
          f"= {sim.size / 1e6:.1f} M pairs in {time.perf_counter() - t0:.2f}s "
          f"({sim.nbytes / 1e6:.0f} MB in memory)")

    np.fill_diagonal(sim, -1)                    # a movie is not its own match
    top_idx = np.argsort(-sim, axis=1)[:, :TOP_K]
    top_score = np.take_along_axis(sim, top_idx, axis=1)
    np.savez_compressed(OUT, idx=top_idx.astype("int16"), score=top_score)
    print(f"Kept top-{TOP_K} neighbours per movie -> {OUT} "
          f"({OUT.stat().st_size / 1e6:.2f} MB)")

    vocab = vectorizer.get_feature_names_out()
    counts = np.asarray(vectors.sum(axis=0)).ravel()
    print("\nMost frequent tag words:", ", ".join(vocab[np.argsort(-counts)[:12]]))
    i = movies.index[movies["title"] == "Avatar"][0]
    words = vocab[vectors[i].nonzero()[1]]
    print(f"Avatar's vector has {len(words)} non-zero words, e.g. "
          f"{', '.join(sorted(words)[:10])} ...")
