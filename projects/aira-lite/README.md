# AIRA-Lite — RAG-based AI Research Assistant (final-year project)

Upload research papers (PDF) and work with them through retrieval-augmented generation: research chat, summaries, literature review, research-gap detection, paper comparison and citations.

**Stack:** FastAPI · SQLAlchemy (async) · Sentence-Transformers `all-MiniLM-L6-v2` · ChromaDB · Google Gemini · React (Vite)

```
backend/app/
├── main.py          FastAPI app: start-up (DB, embedding model), CORS, routers
└── api/papers.py    Upload → background processing (extract → chunk → embed → ChromaDB), list, stats, delete
```

These files are an annotated copy of the AIRA-Lite source: explanatory comments were added for the portfolio walkthrough; the code itself is unchanged. API keys live in `backend/.env`, which is never committed.
