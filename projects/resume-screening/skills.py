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

IN, OUT = Path("build/resumes_clean.json"), Path("build/skills.json")

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
    print(f"\nSaved {OUT}")
