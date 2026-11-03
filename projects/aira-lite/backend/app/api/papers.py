# ============================================================================
# AIRA-Lite - Papers API (backend/app/api/papers.py)
# Everything about the paper library: upload a PDF, process it into
# searchable chunks, list papers, dashboard stats, and delete.
#
# Upload flow (the heart of the RAG "indexing" phase):
#   POST /api/v1/papers/upload
#     -> save the PDF + create a DB row with status "processing"
#     -> respond immediately (the UI does not freeze)
#     -> in the background: extract text -> split into chunks
#        -> embed + store in ChromaDB -> status "ready"
# ============================================================================
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db, AsyncSessionLocal
from app.models.paper import Paper
from app.models.query import QueryLog
from app.services import pdf_service, vector_service
from app.core.config import settings
import os, uuid, logging

# All routes below start with /papers (and /api/v1 is added in main.py)
router = APIRouter(prefix="/papers", tags=["papers"])
logger = logging.getLogger(__name__)


# ── Background processing ───────────────────────────────────────────────────
# FastAPI's BackgroundTasks supports async callables directly — no executor,
# no manual event loop handling needed. This was the root cause of uploads
# silently failing to produce embeddings (the old executor wiring never ran).
async def _process_paper(paper_id: str, file_path: str):
    # The request's DB session is closed once the response is sent, so the
    # background job opens its OWN session.
    async with AsyncSessionLocal() as db:
        paper = await db.get(Paper, paper_id)
        if not paper:
            logger.error(f"Paper {paper_id} disappeared before processing.")
            return
        try:
            # 1) PDF -> text + metadata (title, authors, abstract, year, pages)
            extracted = pdf_service.extract_paper(file_path)
            # 2) Long text -> overlapping chunks (size/overlap from config).
            #    The overlap keeps sentences at chunk borders from being lost.
            chunks = pdf_service.chunk_text(
                extracted.full_text,
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
            )

            # A scanned PDF is just images - no text to embed, so fail clearly
            if not chunks:
                raise ValueError("No extractable text found in PDF (possibly a scanned/image-only PDF).")

            # 3) Embed every chunk (all-MiniLM-L6-v2) and store it in
            #    ChromaDB, tagged with paper_id so we can filter/delete later
            vector_service.add_chunks(paper_id, chunks)

            # 4) Save the extracted metadata and mark the paper "ready"
            #    (this is what turns the badge green in the Upload page)
            paper.title = extracted.title or paper.title
            paper.authors = extracted.authors
            paper.abstract = extracted.abstract
            paper.year = extracted.year
            paper.total_pages = extracted.total_pages
            paper.chunk_count = len(chunks)
            paper.status = "ready"
            await db.commit()
            logger.info(f"✅ Paper {paper_id} ready — {len(chunks)} chunks embedded into ChromaDB")
        except Exception as e:
            # Never leave a paper stuck on "processing": record the error so
            # the UI can show it, and log the full traceback for debugging
            logger.error(f"❌ Processing failed for {paper_id}: {e}", exc_info=True)
            paper.status = "error"
            await db.commit()


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_paper(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),   # FastAPI injects a DB session
):
    # Validate input early and return a clear 400 error
    fname = file.filename or ""
    if not fname.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted (.pdf extension required).")

    content = await file.read()
    if not content:
        raise HTTPException(400, "Uploaded file is empty.")

    # A UUID makes every stored file name unique, even if two users upload
    # papers with the same name
    paper_id = str(uuid.uuid4())
    safe_name = f"{paper_id}_{fname}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as f:
        f.write(content)

    file_size_mb = round(len(content) / (1024 * 1024), 2)

    # Create the DB row first with status "processing" - the UI shows this
    # immediately while the heavy work runs in the background
    paper = Paper(
        id=paper_id,
        title=fname.replace(".pdf", "").replace("_", " "),
        filename=fname,
        file_path=file_path,
        file_size=file_size_mb,
        status="processing",
    )
    db.add(paper)
    await db.commit()
    await db.refresh(paper)

    # Correct usage: pass the async function and its args; FastAPI awaits it
    # after the response is sent. No executor, no manual asyncio handling.
    background_tasks.add_task(_process_paper, paper_id, file_path)

    return {
        "id": paper_id,
        "filename": fname,
        "status": "processing",
        "message": "Upload successful. Processing in background.",
    }


# List every paper, newest first (feeds the "Papers (6)" list in the UI)
@router.get("/")
async def list_papers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Paper).order_by(Paper.created_at.desc()))
    return [_to_dict(p) for p in result.scalars().all()]


# Dashboard numbers - COUNT queries run in the database, not in Python
@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    total_papers = await db.scalar(select(func.count(Paper.id))) or 0
    ready_papers = await db.scalar(select(func.count(Paper.id)).where(Paper.status == "ready")) or 0
    total_queries = await db.scalar(select(func.count(QueryLog.id))) or 0
    total_reviews = await db.scalar(
        select(func.count(QueryLog.id)).where(QueryLog.query_type == "literature_review")
    ) or 0
    return {
        "total_papers": total_papers,
        "ready_papers": ready_papers,
        "total_queries": total_queries,
        "total_reviews": total_reviews,
    }


# Last 10 actions (chat, summary, review ...) for the dashboard feed
@router.get("/recent-activity")
async def recent_activity(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(QueryLog).order_by(QueryLog.created_at.desc()).limit(10))
    return [
        {
            "id": l.id,
            "type": l.query_type,
            "question": (l.question or "")[:120],
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }
        for l in result.scalars().all()
    ]


# NOTE: declared AFTER /stats and /recent-activity - otherwise FastAPI would
# treat the word "stats" as a paper_id
@router.get("/{paper_id}")
async def get_paper(paper_id: str, db: AsyncSession = Depends(get_db)):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found.")
    return _to_dict(paper)


# Delete in three places so nothing is left behind:
# the PDF on disk, its vectors in ChromaDB, and its row in the database
@router.delete("/{paper_id}")
async def delete_paper(paper_id: str, db: AsyncSession = Depends(get_db)):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found.")
    if os.path.exists(paper.file_path):
        os.remove(paper.file_path)
    vector_service.delete_paper_chunks(paper_id)
    await db.delete(paper)
    await db.commit()
    return {"message": "Paper deleted successfully."}


# Convert a database object into plain JSON for the frontend
def _to_dict(p: Paper) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "filename": p.filename,
        "authors": p.authors,
        "abstract": p.abstract,
        "year": p.year,
        "total_pages": p.total_pages,
        "chunk_count": p.chunk_count,
        "file_size": p.file_size,
        "status": p.status,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }
