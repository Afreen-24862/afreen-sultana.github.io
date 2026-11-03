"""
AI Resume Screening Helper - Step 1: Extract text from resumes
==============================================================
Resumes arrive in different formats, so each format gets its own reader:
  * PDF  -> pdfplumber (keeps reading order better than most PDF libraries)
  * DOCX -> python-docx (reads every paragraph of the Word file)
  * TXT  -> plain read
Everything downstream works on plain text, so this is the only step that
needs to know about file formats.
"""
import json
from pathlib import Path

import pdfplumber
from docx import Document

RESUMES = Path("data/resumes")
OUT = Path("build/resumes.json")


def read_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def read_docx(path):
    return "\n".join(p.text for p in Document(path).paragraphs)


def read_txt(path):
    return path.read_text(encoding="utf-8")


READERS = {".pdf": read_pdf, ".docx": read_docx, ".txt": read_txt}


def extract_all(folder=RESUMES):
    results = []
    for path in sorted(folder.iterdir()):
        reader = READERS.get(path.suffix.lower())
        if reader is None:
            print(f"  skipped {path.name} (unsupported format)")
            continue
        text = reader(path)
        results.append({"file": path.name, "format": path.suffix[1:],
                        "candidate": text.strip().splitlines()[0],
                        "text": text})
    return results


if __name__ == "__main__":
    resumes = extract_all()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(resumes, indent=1), encoding="utf-8")

    job = Path("data/job_description.txt").read_text(encoding="utf-8")
    print(f"Job description: {len(job.split())} words "
          f"({job.splitlines()[0]})\n")
    print(f"{'file':<20} {'format':<6} {'words':>5}  candidate")
    for r in resumes:
        print(f"{r['file']:<20} {r['format']:<6} {len(r['text'].split()):>5}  "
              f"{r['candidate']}")
    sample = resumes[0]
    print(f"\nRaw text extracted from {sample['file']} (first 230 chars):")
    print(sample["text"][:230].replace("\n", " | "))
    print(f"\nSaved {OUT}")
