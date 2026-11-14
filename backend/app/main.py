
import uuid

from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import DOCUMENT_DIR, MAX_FILE_SIZE
from app.services.ingestion import extract_pdf
from app.services.embeddings import generate_embeddings
from app.services.vector_store import store_chunks

from pydantic import BaseModel

from app.services.retrieval import retrieve_chunks
from app.services.generation import generate_answer

app = FastAPI(
    title="RFPilot API",
    description="Enterprise RAG Intelligence Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to RFPilot API"
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/api/documents/upload")
def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    document_id = str(uuid.uuid4())

    filename = Path(file.filename).name

    file_path = DOCUMENT_DIR / f"{document_id}.pdf"

    try:

        content = file.file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Maximum file size is 15 MB."
            )

        file_path.write_bytes(content)

        chunks = extract_pdf(file_path)

        texts = [chunk["text"] for chunk in chunks]

        embeddings = []

        for i in range(0, len(texts), 16):

            batch = texts[i:i + 16]

            batch_embeddings = generate_embeddings(batch)

            embeddings.extend(batch_embeddings)

        stored_count = store_chunks(
            chunks,
            embeddings,
            document_id,
            filename
        )

        return {
            "message": "Document processed successfully",
            "document_id": document_id,
            "filename": filename,
            "total_chunks": stored_count
        }

    except HTTPException:
        raise

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    
class ChatRequest(BaseModel):
    question: str
    document_id: str | None = None


@app.post("/api/chat")
def chat_with_documents(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Retrieve relevant document chunks
    context = retrieve_chunks(
        question=request.question,
        document_id=request.document_id,
        top_k=5
    )

    if not context:
        return {
            "answer": "No relevant information was found in the uploaded documents.",
            "sources": []
        }

    # Generate grounded answer
    answer = generate_answer(
        request.question,
        context
    )

    # Prepare source references
    sources = []

    for index, chunk in enumerate(context, start=1):

        sources.append({
            "source": f"Source {index}",
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "content": chunk["text"],
            "retrieval_score": chunk["retrieval_score"]
        })

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }
