# ============================================================================
# AIRA-Lite backend - application entry point (backend/app/main.py)
# Started with:  uvicorn app.main:app --reload
# Responsibilities of this file:
#   1. run start-up work once (database tables, embedding model)
#   2. configure CORS so the React frontend (Vite, port 5173) can call the API
#   3. plug in the route modules: /api/v1/papers and /api/v1/research
# ============================================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# "lifespan" = code that runs once when the server starts (before `yield`)
# and once when it stops (after `yield`). It replaces the older
# @app.on_event("startup") style.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AIRA-Lite backend...")

    # Create the database tables (papers, query logs) if they do not exist.
    # Imports are inside the function so the app object can be created
    # quickly and these modules load only when the server really starts.
    from app.core.database import init_db
    await init_db()
    logger.info("Database initialized")

    # Pre-load embedding model (local, no API key needed)
    # Loading all-MiniLM-L6-v2 takes a few seconds; doing it here means the
    # FIRST user request is fast instead of waiting for the model.
    from app.services.vector_service import get_embedding_model
    get_embedding_model()
    logger.info("Embedding model loaded (all-MiniLM-L6-v2)")

    # Warn loudly (but don't crash) if Gemini isn't configured —
    # uploads/browsing still work, only generation endpoints need this.
    from app.core.config import settings
    if not settings.GEMINI_API_KEY:
        logger.warning(
            "⚠️  GEMINI_API_KEY is not set in backend/.env — "
            "Chat, Summary, Literature Review, Gaps, Compare, and Citation "
            "endpoints will fail until you add a key from "
            "https://aistudio.google.com/app/apikey"
        )
    else:
        logger.info(f"Gemini configured — model: {settings.GEMINI_MODEL}")

    yield  # <- the server handles requests while paused here
    logger.info("Shutting down AIRA-Lite backend")


# The FastAPI application. Title/description/version also appear in the
# automatic API docs at http://localhost:8000/docs
app = FastAPI(
    title="AIRA-Lite API",
    description="AI-Powered Research Assistant using RAG (Gemini + ChromaDB + Sentence Transformers)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: explicit origins only. "*" combined with allow_credentials=True is
# rejected by browsers, so list the dev origins explicitly instead.
# (The browser blocks calls from localhost:5173 to localhost:8000 unless the
# API says that origin is allowed - this middleware adds those headers.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers keep the code organised by feature:
#   papers   -> upload, list, stats, delete     (/api/v1/papers/...)
#   research -> chat, summary, review, gaps,
#               compare, citations              (/api/v1/research/...)
from app.api.papers import router as papers_router
from app.api.research import router as research_router

app.include_router(papers_router, prefix="/api/v1")
app.include_router(research_router, prefix="/api/v1")


# Simple "is it up?" endpoint
@app.get("/")
async def root():
    return {"message": "AIRA-Lite API is running", "version": "1.0.0"}


# Health check used by the frontend: tells the UI whether Gemini is set up,
# so it can show a clear message instead of failing silently.
@app.get("/health")
async def health():
    from app.core.config import settings
    return {
        "status": "healthy",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "gemini_model": settings.GEMINI_MODEL,
    }
