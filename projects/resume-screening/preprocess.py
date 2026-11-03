"""
AI Resume Screening Helper - Step 2: Clean and normalise the text
=================================================================
  1. Remove personal details (emails, phone numbers, links). They carry no
     skill information, and removing them reduces bias in scoring.
  2. Lower-case everything so "Python" and "python" are the same word.
  3. Tokenise while KEEPING tech symbols intact: "scikit-learn", "ci/cd",
     "node.js" and "c++" must stay single tokens.
  4. Drop stop-words ("the", "with", "and") that appear in every document.
"""
import json
import re
from pathlib import Path

IN, OUT = Path("build/resumes.json"), Path("build/resumes_clean.json")

EMAIL = re.compile(r"\S+@\S+")
PHONE = re.compile(r"\+?\d[\d\s-]{8,}\d")
URL = re.compile(r"(https?://|www\.|linkedin\.com|github\.com)\S*")
TOKEN = re.compile(r"[a-z0-9][a-z0-9+#./-]*[a-z0-9+#]|[a-z0-9]")
STOP_WORDS = set("""a an and are as at be by for from has have in is it its of
on or that the to was were will with you your we our this using used into
over per who which""".split())


def clean(text):
    text = EMAIL.sub(" ", text)
    text = PHONE.sub(" ", text)
    text = URL.sub(" ", text)
    text = re.sub(r"[|•·]", " ", text)                # layout separators
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(clean_text):
    return [t for t in TOKEN.findall(clean_text) if t not in STOP_WORDS]


if __name__ == "__main__":
    resumes = json.loads(IN.read_text(encoding="utf-8"))
    job_raw = Path("data/job_description.txt").read_text(encoding="utf-8")
    docs = resumes + [{"file": "job_description.txt",
                       "candidate": "JOB", "text": job_raw}]

    for d in docs:
        d["clean"] = clean(d["text"])
        d["tokens"] = tokenize(d["clean"])
    OUT.write_text(json.dumps(docs, indent=1), encoding="utf-8")

    sample = docs[0]
    print(f"Before ({sample['file']}): {sample['text'][:120]!r}")
    print(f"After  ({sample['file']}): {sample['clean'][:120]!r}\n")
    print("Removed: email, phone number and LinkedIn link")
    special = [t for t in sample["tokens"] if any(c in t for c in "-./+")]
    print(f"Tokens kept intact: {list(dict.fromkeys(special))}\n")
    for d in docs:
        print(f"  {d['candidate']:<15} {len(d['text'].split()):>3} words -> "
              f"{len(d['tokens']):>3} tokens")
    print(f"\nSaved {OUT}")
