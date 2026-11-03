# AI Resume Screening Helper

Scores resumes against a job description and explains every score.

| Step | File | What it does |
|---|---|---|
| 1 | `extract_text.py` | PDF (pdfplumber), DOCX (python-docx) and TXT → text |
| 2 | `preprocess.py` | Remove personal details, normalise, tokenise (keeps scikit-learn, ci/cd intact) |
| 3 | `skills.py` | Skill dictionary with synonyms, word-boundary matching |
| 4 | `matcher.py` | 70% required + 20% nice-to-have + 10% TF-IDF similarity |
| 5 | `rank.py` | Ranking, shortlist rule, CSV report and chart |

The resumes in `data/resumes/` are fictional samples for the demo.
