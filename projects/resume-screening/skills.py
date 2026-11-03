"""
AI Resume Screening Helper - Step 3: Extract skills
===================================================
Keyword matching with a SKILL DICTIONARY. Each canonical skill has the
different ways people write it ("ml", "machine learning"; "postgresql",
"mysql" -> SQL). Matching uses word boundaries so "java" does not match
inside "javascript", and "r" is not found inside every word.

The same function reads the job description, so resumes and job are
compared in the same vocabulary.
"""
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors  # noqa: E402,F401
import matplotlib.pyplot as plt  # noqa: E402

IN, OUT = Path("build/resumes_clean.json"), Path("build/skills.json")
CHART = Path("outputs/resume_skill_matrix.png")

SKILLS = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "rest apis": ["rest api", "rest apis", "restful"],
    "git": ["git", "github", "gitlab"],
    "docker": ["docker", "containerised", "containerized"],
    "aws": ["aws", "amazon web services", "ec2", "s3"],
    "nlp": ["nlp", "natural language processing"],
    "llm": ["llm", "llms", "generative ai", "genai"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "ci/cd": ["ci/cd", "jenkins", "github actions"],
    "java": ["java", "spring boot"],
    "javascript": ["javascript", "react", "node.js"],
    "power bi": ["power bi", "tableau"],
}


def find_skills(clean_text):
    found = set()
    for skill, variants in SKILLS.items():
        for v in variants:
            # (?<![\w-]) / (?![\w-]) = word boundary that also respects "-"
            if re.search(rf"(?<![\w-]){re.escape(v)}(?![\w-])", clean_text):
                found.add(skill)
                break
    return sorted(found)


def job_requirements(raw_job_text):
    """Split the job post into required and nice-to-have skills."""
    lower = raw_job_text.lower()
    required = lower.split("required skills:")[1].split("nice to have:")[0]
    nice = lower.split("nice to have:")[1].split("experience:")[0]
    return find_skills(required), find_skills(nice)


if __name__ == "__main__":
    docs = json.loads(IN.read_text(encoding="utf-8"))
    job = next(d for d in docs if d["candidate"] == "JOB")
    required, nice = job_requirements(job["text"])
    print(f"Skill dictionary: {len(SKILLS)} skills, "
          f"{sum(len(v) for v in SKILLS.values())} spellings")
    print(f"\nJob requires ({len(required)}): {', '.join(required)}")
    print(f"Nice to have ({len(nice)}):  {', '.join(nice)}\n")

    result = {"required": required, "nice": nice, "candidates": []}
    for d in docs:
        if d["candidate"] == "JOB":
            continue
        skills = find_skills(d["clean"])
        result["candidates"].append({"candidate": d["candidate"],
                                     "file": d["file"], "skills": skills,
                                     "clean": d["clean"]})
        print(f"{d['candidate']:<15} ({len(skills):>2}) {', '.join(skills)}")
    OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")

    # ---- Chart: candidate x skill matrix (green = has the skill) ----
    cols = required + nice
    rows = result["candidates"]
    grid = [[1 if skill in c["skills"] else 0 for skill in cols] for c in rows]
    fig, ax = plt.subplots(figsize=(10, 2.9), dpi=120)
    ax.imshow(grid, cmap=matplotlib.colors.ListedColormap(["#f2f2f7", "#30d158"]),
              aspect="auto")
    for i, row in enumerate(grid):
        for j, has in enumerate(row):
            ax.text(j, i, "✓" if has else "–", ha="center", va="center",
                    fontsize=10, color="white" if has else "#aeaeb2")
    ax.set_xticks(range(len(cols)), cols, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(rows)), [c["candidate"] for c in rows], fontsize=9)
    ax.axvline(len(required) - 0.5, color="#1d1d1f", lw=1.5)   # required | nice
    ax.set_title(f"Skill matrix - required ({len(required)}) | "
                 f"nice to have ({len(nice)})", fontsize=10)
    CHART.parent.mkdir(exist_ok=True)
    fig.savefig(CHART, bbox_inches="tight")
    print(f"\nSaved {OUT} | Chart: {CHART}")
