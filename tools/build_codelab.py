"""
Build the "Code walkthrough" data for the portfolio.

For every project in projects/ this script:
  1. runs each module in order (python <file>) and captures what it prints,
     how long it took, and the charts it saved,
  2. syntax-highlights the source with Pygments,
  3. writes everything to js/codelab-data.js, which js/codelab.js renders.

Run from the repository root:   python tools/build_codelab.py
Only needed when project code changes - the website itself stays static.
"""
import ast
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

from PIL import Image
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/Afreen-24862/afreen-sultana.github.io/tree/main/"

# --------------------------------------------------------------------------
# Project + module descriptions (what the page shows next to the code)
# --------------------------------------------------------------------------
PROJECTS = [
    {
        "id": "aira", "slug": "aira-lite", "run": False,
        "name": "AIRA", "sub": "RAG-based AI Research Agent · AIRA-Lite",
        "badge": "Final-year project",
        "stack": ["Python", "FastAPI", "RAG", "Sentence-Transformers",
                  "ChromaDB", "Gemini LLM", "React (Vite)", "SQLAlchemy"],
        "data": "Research papers uploaded as PDFs (BERT, ResNet, GANs, "
                "DQN Atari ...)",
        "kpis": [("6", "papers indexed"), ("16", "chunks for BERT alone"),
                 ("384-d", "MiniLM embeddings"), ("7", "research tools")],
        "modules": [
            {"file": "backend/app/main.py", "title": "API start-up",
             "key": "lifespan",
             "does": "Starts the FastAPI server: creates the database "
                     "tables, pre-loads the MiniLM embedding model, enables "
                     "CORS for the React app and mounts the papers and "
                     "research routers.",
             "notes": ["Pre-loading the embedding model at start-up keeps "
                       "the first user request fast.",
                       "Missing Gemini key = warning, not a crash: upload "
                       "and browsing still work."],
             "cmd": "uvicorn app.main:app --reload",
             "imgs": [("aira/sidebar.jpg", "The React app shell served "
                       "against this API: every research tool available, "
                       "status 'RAG Pipeline Active - Powered by ChromaDB + "
                       "Gemini'", False)]},
            {"file": "backend/app/api/papers.py",
             "title": "Upload & index papers", "key": "_process_paper",
             "does": "Accepts a PDF, saves it, responds immediately, then "
                     "in the background extracts text, splits it into "
                     "overlapping chunks, embeds them into ChromaDB and "
                     "marks the paper ready.",
             "notes": ["Background task = the upload request returns in "
                       "milliseconds; indexing happens after the response.",
                       "Delete removes the PDF, its vectors and its DB row - "
                       "nothing is left behind."],
             "cmd": "POST /api/v1/papers/upload",
             "imgs": [("aira/upload.jpg", "Upload page: 6 papers processed "
                       "- BERT parsed to 16 pages, 16 chunks indexed, "
                       "status Ready")]},
            {"file": None, "label": "/chat", "title": "Research Chat",
             "does": "Ask questions across the uploaded papers. AIRA finds "
                     "the most relevant passages and generates an answer "
                     "grounded in them.",
             "notes": ["Selecting papers narrows the search; with none "
                       "selected it searches the whole library.",
                       "Suggested questions (main contribution, methodology, "
                       "key findings) help first-time users start."],
             "cmd": "localhost:5173/chat",
             "imgs": [("aira/chat.jpg", "Research Chat - RAG question "
                       "answering across uploaded papers")]},
            {"file": None, "label": "/summary", "title": "Summarize paper",
             "does": "Pick one paper and AIRA produces a structured "
                     "summary covering objectives, methodology, findings and "
                     "contributions.",
             "notes": ["Fixed sections make summaries easy to compare "
                       "across papers."],
             "cmd": "localhost:5173/summary",
             "imgs": [("aira/summary.jpg", "Summarize Paper - choose one "
                       "paper, then Generate Summary")]},
            {"file": None, "label": "/review", "title": "Literature review",
             "does": "Select two or more papers and AIRA synthesises themes, "
                     "methodologies, findings and research gaps into a "
                     "structured academic review.",
             "notes": ["A minimum of 2 papers is enforced - a review needs "
                       "something to synthesise.",
                       "Each review is logged and counted on the dashboard "
                       "(the /papers/stats endpoint)."],
             "cmd": "localhost:5173/review",
             "imgs": [("aira/review.jpg", "Literature Review - select at "
                       "least 2 papers, then Generate Review")]},
            {"file": None, "label": "/gaps", "title": "Research gaps",
             "does": "AIRA analyses limitations, future-work sections and "
                     "methodology gaps across the selected papers to surface "
                     "unexplored research opportunities.",
             "notes": ["Useful for choosing a thesis or project topic."],
             "cmd": "localhost:5173/gaps",
             "imgs": [("aira/gaps.jpg", "Research Gap Detection - select "
                       "papers, then Detect Gaps")]},
            {"file": None, "label": "/compare", "title": "Compare papers",
             "does": "Select 2-4 papers for a side-by-side comparison table "
                     "of objectives, methodology, results and limitations.",
             "notes": ["The 2-4 paper limit keeps the comparison table "
                       "readable."],
             "cmd": "localhost:5173/compare",
             "imgs": [("aira/compare.jpg", "Compare Papers - select 2-4 "
                       "papers, then Compare Papers")]},
            {"file": None, "label": "/citations", "title": "Citations & questions",
             "does": "Generates a formatted citation (APA and other styles) "
                     "for a paper, and formulates new research questions for "
                     "a chosen topic from the selected papers.",
             "notes": ["Paper metadata (title, authors, year) is extracted "
                       "from the PDF at upload - see step 2."],
             "cmd": "localhost:5173/citations",
             "imgs": [("aira/citations.jpg", "Citations & Research "
                       "Questions - citation generator (left) and research "
                       "question generator (right)")]},
        ],
    },
    {
        "id": "cityair", "slug": "cityair", "run": True,
        "name": "CityAir AI", "sub": "Hyderabad air-quality forecasting "
                                      "+ LLM assistant",
        "stack": ["Python", "Pandas", "scikit-learn", "Matplotlib",
                  "Gemini LLM"],
        "data": "CPCB daily readings for Hyderabad, 2015-2020 (Kaggle: "
                "Air Quality Data in India)",
        "kpis": [("load_data.py", r"Rows: ([\d,]+)", "{}", "days of data"),
                 ("train_model.py", r"(\d+)% lower error", "{}%",
                  "better than baseline"),
                 ("train_model.py", r"Random Forest\s+([\d.]+)", "{}",
                  "MAE (AQI points)"),
                 ("eda.py", r"AQI\s+[\d.]+ ->\s+[\d.]+\s+\((-?[\d.]+)%\)",
                  "{}%", "AQI in 2020 lockdown")],
        "modules": [
            {"file": "load_data.py", "title": "Load the data", "key": "main",
             "does": "Reads 5½ years of daily Hyderabad readings and "
                     "profiles them: period, missing dates, missing values "
                     "per pollutant and how often each AQI category occurs.",
             "notes": ["Explore before cleaning - the missing-value profile "
                       "(PM10 and NH3 ~18% empty) decides the strategy.",
                       "Most days are Moderate or Satisfactory; Poor and "
                       "worse are rare but matter most to residents."]},
            {"file": "clean_features.py", "title": "Clean + features",
             "key": "add_features",
             "does": "Fills short sensor gaps, caps extreme spikes, and "
                     "builds lag, rolling-mean and season features with "
                     "tomorrow's AQI as the target.",
             "notes": ["Only gaps of 3 days or less are interpolated - "
                       "longer gaps are dropped, never invented.",
                       "shift(-1) makes the target, shift(+1/+7) makes lags: "
                       "no future value leaks into the inputs."]},
            {"file": "eda.py", "title": "Find the patterns", "key": "main",
             "does": "Yearly trend, seasons, the pollutant that drives AQI, "
                     "and the 2020 lockdown as a natural experiment.",
             "notes": ["Winter is worst, monsoon cleanest - rain washes "
                       "particles out of the air.",
                       "PM2.5 has the strongest link with AQI (r = 0.78), so "
                       "the assistant talks about it most."]},
            {"file": "train_model.py", "title": "Forecast tomorrow",
             "key": "main",
             "does": "Trains Linear Regression and Random Forest on "
                     "2015-2019, tests on unseen 2020, and compares both "
                     "with a 'tomorrow = today' baseline.",
             "notes": ["Time-based split: a random split would let the "
                       "model peek at the future and inflate the score.",
                       "Predicting the CHANGE instead of the level is what "
                       "let the forest beat the baseline."]},
            {"file": "assistant.py", "title": "LLM assistant",
             "key": "build_fact_sheet",
             "does": "Builds a fact sheet from the data and the forecast "
                     "model, puts it in a grounded prompt and asks Gemini. "
                     "Without an API key a rule-based fallback answers from "
                     "the same facts.",
             "notes": ["Grounding: the LLM may only use our numbers, so it "
                       "cannot invent AQI values.",
                       "This recording ran without an API key, so the "
                       "answers below come from the offline fallback."]},
        ],
    },
    {
        "id": "student", "slug": "student-performance", "run": True,
        "name": "Student Performance", "sub": "Predict pass / fail and "
                                              "flag at-risk students",
        "stack": ["Python", "Pandas", "NumPy", "scikit-learn", "Matplotlib"],
        "data": "UCI Student Performance dataset - 395 students, 33 "
                "attributes (maths course)",
        "kpis": [("load_data.py", r"Shape: (\d+) students", "{}", "students"),
                 ("evaluate.py", r"accuracy\s+0\.(\d+)", "{}%",
                  "test accuracy"),
                 ("train.py", r"with term grades it catches (\d+)%", "{}%",
                  "at-risk students caught"),
                 ("preprocess.py", r"after encoding: (\d+)", "{}",
                  "features after encoding")],
        "modules": [
            {"file": "load_data.py", "title": "Load & profile",
             "key": "main",
             "does": "Loads the UCI dataset (';'-separated), checks types "
                     "and missing values, and defines the target: pass if "
                     "the final grade G3 is 10 or more out of 20.",
             "notes": ["67% pass / 33% fail - imbalanced, so accuracy alone "
                       "would be misleading.",
                       "38 students scored 0: most likely absent from the "
                       "exam, worth mentioning as a data-quality caveat."]},
            {"file": "preprocess.py", "title": "Encode features",
             "key": "preprocess",
             "does": "Creates the pass/fail target, converts yes/no and "
                     "two-option columns to 1/0, one-hot encodes the rest "
                     "and removes G3 from the inputs.",
             "notes": ["Dropping G3 prevents target leakage - it IS the "
                       "answer.",
                       "drop_first=True avoids a redundant dummy column."]},
            {"file": "eda.py", "title": "Explore drivers", "key": "main",
             "does": "Correlations with passing, pass rate by past "
                     "failures and study time, and how term grades track "
                     "the final grade.",
             "notes": ["Past failures are the strongest warning sign: 75% "
                       "pass with none, 18% with two.",
                       "G2 correlates 0.90 with G3, which is why we test "
                       "with and without term grades."]},
            {"file": "train.py", "title": "Train & compare",
             "key": "run_scenario",
             "does": "Compares a baseline, Logistic Regression, Decision "
                     "Tree and Random Forest with 5-fold cross-validation, "
                     "in an early-warning and a with-grades scenario.",
             "notes": ["The model is chosen by cross-validation, never by "
                       "the test score.",
                       "Honest result: without grades only ~46% of failing "
                       "students are caught; with grades 92%."]},
            {"file": "evaluate.py", "title": "Evaluate", "key": "main",
             "does": "Classification report, confusion matrix and feature "
                     "importance for the chosen Random Forest.",
             "notes": ["The costly mistake is a failing student predicted "
                       "to pass - only 2 of 26 here.",
                       "Feature importance makes the model explainable to "
                       "teachers."]},
            {"file": "predict.py", "title": "Predict new students",
             "key": "main",
             "does": "Applies exactly the same preprocessing to new "
                     "students and returns the probability of passing with "
                     "a risk label.",
             "notes": ["Re-using preprocess() guarantees training and "
                       "prediction encode data the same way.",
                       "Output is an action: high-risk students get "
                       "mentoring."]},
        ],
    },
    {
        "id": "reelpick", "slug": "reelpick", "run": True,
        "name": "ReelPick", "sub": "Content-based movie recommender",
        "stack": ["Python", "Pandas", "scikit-learn", "NumPy", "Streamlit"],
        "data": "TMDB 5000 Movies dataset (Kaggle) - movies + credits",
        "kpis": [("preprocess.py", r"Movies with tags: ([\d,]+)", "{}",
                  "movies"),
                 ("vectorize.py", r"x ([\d,]+) words", "{}",
                  "word vocabulary"),
                 ("vectorize.py", r"= ([\d.]+) M pairs", "{} M",
                  "pairs compared"),
                 ("vectorize.py", r"pairs in ([\d.]+)s", "{} s",
                  "to compare them")],
        "modules": [
            {"file": "load_data.py", "title": "Load movies", "key": "load",
             "does": "Reads the movies and credits files and joins them on "
                     "the movie id - one row per movie.",
             "notes": ["Genres, keywords, cast and crew arrive as JSON text "
                       "and are parsed in the next step."]},
            {"file": "preprocess.py", "title": "Build tags",
             "key": "build_tags",
             "does": "Parses the JSON columns and builds one 'tags' text per "
                     "movie: overview + genres + keywords + top-3 cast + "
                     "director.",
             "notes": ["Names are squashed into one token (christianbale) "
                       "so first names don't create false matches."]},
            {"file": "vectorize.py", "title": "Vectorise + similarity",
             "key": "main",
             "does": "CountVectorizer turns tags into word-count vectors; "
                     "cosine similarity compares every pair of movies; the "
                     "top-30 neighbours are saved.",
             "notes": ["Cosine ignores text length - only the mix of words "
                       "matters.",
                       "Keeping the top-30 neighbours shrinks 92 MB to "
                       "0.5 MB."]},
            {"file": "recommend.py", "title": "recommend()",
             "key": "recommend",
             "does": "Fuzzy-matches the title, then returns the most similar "
                     "movies that pass a minimum-votes quality filter.",
             "notes": ["'Toy Strory' still works thanks to difflib fuzzy "
                       "matching.",
                       "Limitation to discuss: Toy Story -> 40 Year Old "
                       "Virgin, because both overviews mention 'Andy'."]},
            {"file": "app.py", "title": "Streamlit app", "key": None,
             "run": False, "preview": "reelpick",
             "cmd": "streamlit run app.py",
             "does": "A small web UI: pick a movie, choose how many "
                     "suggestions and a vote filter, get recommendation "
                     "cards.",
             "notes": ["Streamlit re-runs the script on every click, so data "
                       "loading is cached."]},
        ],
    },
    {
        "id": "resume", "slug": "resume-screening", "run": True,
        "name": "Resume Screening", "sub": "AI Resume Screening Helper",
        "stack": ["Python", "NLP", "Keyword matching", "scikit-learn",
                  "pdfplumber", "python-docx"],
        "data": "A job description + 4 sample resumes (PDF, DOCX, TXT)",
        "kpis": [("3", "file formats: PDF, DOCX, TXT"),
                 ("skills.py", r"(\d+) skills, \d+ spellings", "{}",
                  "skills in dictionary"),
                 ("rank.py", r"1\s+Ananya Rao\s+([\d.]+)", "{}",
                  "top score / 100"),
                 ("rank.py", r"Shortlisted (\d of \d)", "{}",
                  "shortlisted")],
        "modules": [
            {"file": "extract_text.py", "title": "Extract text",
             "key": "extract_all",
             "does": "Reads PDF (pdfplumber), Word (python-docx) and text "
                     "resumes into plain text.",
             "notes": ["Only this step knows about file formats - everything "
                       "after works on text."]},
            {"file": "preprocess.py", "title": "Clean text", "key": "clean",
             "does": "Removes emails, phone numbers and links, lower-cases, "
                     "and tokenises while keeping tech terms like "
                     "scikit-learn and ci/cd intact.",
             "notes": ["Removing personal details reduces bias in "
                       "scoring."]},
            {"file": "skills.py", "title": "Extract skills",
             "key": "find_skills",
             "does": "Matches a skill dictionary with synonyms (mysql -> "
                     "SQL, github -> Git) using word boundaries, for resumes "
                     "and the job description alike.",
             "notes": ["Word boundaries stop 'java' matching inside "
                       "'javascript'."]},
            {"file": "matcher.py", "title": "Score vs job", "key": "score",
             "does": "Score = 70% required skills + 20% nice-to-have + 10% "
                     "TF-IDF text similarity, with matched and missing "
                     "skills listed.",
             "notes": ["Transparent weights: every score can be explained "
                       "to a recruiter."]},
            {"file": "rank.py", "title": "Rank & shortlist", "key": "main",
             "does": "Sorts candidates, applies the shortlist rule and "
                     "writes a CSV report and a chart.",
             "notes": ["The tool assists - a person makes the final "
                       "decision."]},
        ],
    },
]


# --------------------------------------------------------------------------
def highlight_lines(code):
    # classprefix keeps token classes (k, s, mb ...) from clashing with site CSS
    out = highlight(code, PythonLexer(),
                    HtmlFormatter(nowrap=True, classprefix="tk-"))
    # names, punctuation and spaces have no colour -> plain text (smaller file)
    out = re.sub(r'<span class="tk-(?:n|p|w)">([^<]*)</span>', r"\1", out)
    return out.rstrip("\n").split("\n")


def key_range(code, key):
    """Line range (1-based) of a function, or of the __main__ block."""
    if not key:
        return None
    tree = ast.parse(code)
    for node in tree.body:
        if key == "main" and isinstance(node, ast.If) and \
                "__main__" in ast.unparse(node.test):
            return [node.lineno, node.end_lineno]
        if getattr(node, "name", None) == key:
            start = min([node.lineno] + [d.lineno for d in
                                         getattr(node, "decorator_list", [])])
            return [start, node.end_lineno]
    raise ValueError(f"key {key!r} not found")


def save_chart(src, project_id):
    dest_dir = ROOT / "assets" / "codelab" / project_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    img = Image.open(src).convert("RGB")
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(
        dest, optimize=True)
    return f"assets/codelab/{project_id}/{src.name}"


def run_module(folder, file):
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8",
               GEMINI_API_KEY="")
    before = {p: p.stat().st_mtime for p in (folder / "outputs").glob("*.png")} \
        if (folder / "outputs").exists() else {}
    t0 = time.perf_counter()
    proc = subprocess.run([sys.executable, file], cwd=folder, env=env,
                          capture_output=True, text=True, timeout=600)
    secs = time.perf_counter() - t0
    if proc.returncode != 0:
        raise SystemExit(f"{folder.name}/{file} failed:\n{proc.stderr}")
    charts = [p for p in sorted((folder / "outputs").glob("*.png"))
              if p.stat().st_mtime != before.get(p)] \
        if (folder / "outputs").exists() else []
    return proc.stdout.rstrip(), round(secs, 2), charts


def reelpick_preview(folder):
    """HTML preview of the Streamlit app, filled with real recommend()
    output (Streamlit itself is not run during the build)."""
    code = ("import json; from recommend import recommend; "
            "print(json.dumps(recommend('The Dark Knight Rises', n=5)))")
    out = subprocess.run([sys.executable, "-c", code], cwd=folder,
                         capture_output=True, text=True, check=True).stdout
    title, picks = json.loads(out)
    cards = "".join(
        f'<div class="st-card"><div><b>{html.escape(p["title"])}</b> '
        f'({p["year"]})<small>{html.escape(p["genres"])}</small>'
        f'<i style="width:{min(p["match"] * 200, 100):.0f}%"></i>'
        f'<em>⭐ {p["rating"]:.1f} / 10</em></div>'
        f'<span>Match<b>{p["match"]:.0%}</b></span></div>' for p in picks)
    return (f'<div class="st"><h4>🎬 ReelPick</h4><p class="st-cap">'
            f'Content-based movie recommendations - TMDB 5000 dataset</p>'
            f'<label>Pick a movie you like</label><div class="st-sel">'
            f'{html.escape(title)}<span>▾</span></div>'
            f'<div class="st-row"><label>How many suggestions? <b>5</b>'
            f'</label><label>Minimum votes <b>200</b></label></div>'
            f'<button>Recommend</button><h5>Because you liked '
            f'{html.escape(title)}</h5>{cards}</div>')


def build():
    data = {"generated": date.today().isoformat(),
            "python": sys.version.split()[0], "projects": []}
    for proj in PROJECTS:
        folder = ROOT / "projects" / proj["slug"]
        if proj["run"]:
            for d in ("build", "outputs"):
                shutil.rmtree(folder / d, ignore_errors=True)
        mods, outputs_by_file = [], {}
        for m in proj["modules"]:
            entry = {k: m.get(k) for k in ("title", "does", "notes")}
            entry["file"] = m["file"]
            entry["label"] = m.get("label")
            if m["file"]:
                code = (folder / m["file"]).read_text(encoding="utf-8")
                entry.update(
                    path=f"projects/{proj['slug']}/{m['file']}",
                    lines=code.count("\n") + 1,
                    code=highlight_lines(code),
                    key=key_range(code, m.get("key")))
            entry["cmd"] = m.get("cmd") or f"python {m['file']}"
            # a third item False keeps an image out of the project gallery
            entry["imgs"] = [{"src": f"assets/codelab/{img[0]}", "cap": img[1],
                              "gal": len(img) < 3 or img[2]}
                             for img in m.get("imgs", [])]
            if proj["run"] and m.get("run", True):
                out, secs, charts = run_module(folder, m["file"])
                outputs_by_file[m["file"]] = out
                entry.update(out=out, secs=secs, ran=True)
                entry["imgs"] += [{"src": save_chart(c, proj["id"]),
                                   "cap": c.name, "gal": True} for c in charts]
                print(f"  ran {proj['slug']}/{m['file']} in {secs:.2f}s")
            else:
                entry["ran"] = False
            if m.get("preview") == "reelpick":
                entry["preview"] = reelpick_preview(folder)
            mods.append(entry)

        kpis = []
        for k in proj["kpis"]:
            if len(k) == 2:
                kpis.append({"v": k[0], "l": k[1]})
                continue
            file, pattern, fmt, label = k
            match = re.search(pattern, outputs_by_file[file])
            if not match:
                raise SystemExit(f"KPI {label!r} not found in {file}")
            kpis.append({"v": fmt.format(match.group(1)), "l": label})

        data["projects"].append({
            "id": proj["id"], "name": proj["name"], "sub": proj["sub"],
            "badge": proj.get("badge"), "stack": proj["stack"],
            "data": proj["data"], "kpis": kpis, "modules": mods,
            "folder": REPO + "projects/" + proj["slug"],
            "loc": sum(m.get("lines", 0) for m in mods),
        })

    js = "window.CODELAB = " + json.dumps(data, ensure_ascii=False) + ";\n"
    (ROOT / "js" / "codelab-data.js").write_text(js, encoding="utf-8")
    print(f"Wrote js/codelab-data.js ({len(js) / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
