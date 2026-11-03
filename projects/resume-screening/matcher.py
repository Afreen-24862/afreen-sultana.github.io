"""
AI Resume Screening Helper - Step 4: Score each resume against the job
======================================================================
Relevance score (0-100) =
    70% x required skills covered     <- must-haves matter most
  + 20% x nice-to-have skills covered
  + 10% x TF-IDF text similarity      <- overall wording overlap, catches
                                         context the skill list misses
The weights are a transparent business rule a recruiter can read and
change - every score can be explained line by line.
"""
import json
from pathlib import Path

import matplotlib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import clean

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

IN, OUT = Path("build/skills.json"), Path("build/scores.json")
CHART = Path("outputs/resume_score_breakdown.png")
WEIGHTS = {"required": 0.7, "nice": 0.2, "text": 0.1}


def text_similarity(job_text, resume_texts):
    # TF-IDF down-weights words that are common to every document
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = tfidf.fit_transform([job_text] + resume_texts)
    return cosine_similarity(matrix[0], matrix[1:])[0]


def score(candidate, required, nice, similarity):
    have = set(candidate["skills"])
    req_hit = [s for s in required if s in have]
    nice_hit = [s for s in nice if s in have]
    parts = {"required": len(req_hit) / len(required),
             "nice": len(nice_hit) / len(nice),
             "text": similarity}
    total = 100 * sum(WEIGHTS[k] * v for k, v in parts.items())
    return {"candidate": candidate["candidate"], "file": candidate["file"],
            "score": round(total, 1),
            "parts": {k: round(v, 2) for k, v in parts.items()},
            "matched": req_hit + nice_hit,
            "missing_required": [s for s in required if s not in have]}


if __name__ == "__main__":
    data = json.loads(IN.read_text(encoding="utf-8"))
    job_text = clean(Path("data/job_description.txt").read_text("utf-8"))
    cands = data["candidates"]
    sims = text_similarity(job_text, [c["clean"] for c in cands])

    results = [score(c, data["required"], data["nice"], s)
               for c, s in zip(cands, sims)]
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")

    print(f"Weights: {WEIGHTS}\n")
    for r in results:
        p = r["parts"]
        print(f"{r['candidate']}  ->  {r['score']}/100")
        print(f"  required {p['required']:.0%} x 70  +  nice {p['nice']:.0%} x 20"
              f"  +  text {p['text']:.2f} x 10")
        print(f"  matched: {', '.join(r['matched']) or '-'}")
        print(f"  missing must-haves: {', '.join(r['missing_required']) or 'none'}\n")
    # ---- Chart: where each candidate's points come from ----
    fig, ax = plt.subplots(figsize=(9, 2.9), dpi=120)
    names = [r["candidate"] for r in results][::-1]
    left = [0] * len(results)
    for part, color, label in [("required", "#0071e3", "Required skills (70)"),
                               ("nice", "#5ac8fa", "Nice to have (20)"),
                               ("text", "#bf5af2", "Text similarity (10)")]:
        pts = [100 * WEIGHTS[part] * r["parts"][part] for r in results][::-1]
        ax.barh(names, pts, left=left, color=color, label=label)
        left = [a + b for a, b in zip(left, pts)]
    for i, total in enumerate(left):
        ax.text(total + 1, i, f"{total:.0f}", va="center", fontsize=9)
    ax.set_xlim(0, 100)
    ax.legend(fontsize=8, frameon=False, ncol=3, loc="lower right",
              bbox_to_anchor=(1, 1.02))
    ax.set_title("Score breakdown (points out of 100)", fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    CHART.parent.mkdir(exist_ok=True)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"Saved {OUT} | Chart: {CHART}")
