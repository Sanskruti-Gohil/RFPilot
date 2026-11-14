# RFPilot – Enterprise RAG & Solution Intelligence Platform

An open-source AI-powered platform designed to analyse business documents, extract requirements, retrieve relevant information, and generate evidence-grounded responses using Retrieval-Augmented Generation (RAG).

## Overview

RFPilot aims to simplify enterprise document analysis by allowing users to upload business documents and interact with their contents through an AI-powered question-answering system.

The platform combines semantic search, keyword retrieval, vector storage, and locally running language models to provide context-aware responses with document source references.

The project is being developed with a focus on AI engineering, full-stack development, and practical enterprise applications.

## Key Features

- PDF document upload
- Automated text extraction
- Overlapping text chunking
- Local embedding generation
- Persistent vector storage
- Hybrid retrieval using BM25 and semantic search
- LLM-powered document question answering
- Document source references with page numbers
- Local LLM inference without paid API dependencies

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| LLM Runtime | Ollama |
| Language Model | Qwen3 1.7B |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Keyword Retrieval | BM25 |
| PDF Processing | PyPDF |
| Development | Git, GitHub |

## Architecture

The current RAG pipeline follows this workflow:

1. Upload a PDF document.
2. Extract text using PyPDF.
3. Divide the extracted text into overlapping chunks.
4. Generate embeddings locally using Ollama.
5. Store document chunks and embeddings in ChromaDB.
6. Retrieve relevant chunks using semantic and keyword search.
7. Pass the retrieved context to the local language model.
8. Generate an answer with supporting document references.

## Project Structure

```text
RFPilot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
├── docs/
├── storage/
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11
- Node.js LTS
- Ollama
- Git

### Clone the repository

```bash
git clone https://github.com/Sanskruti-Gohil/RFPilot.git
cd RFPilot
```

### Backend setup

```bash
cd backend

python -m venv venv

# Windows PowerShell
.\venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Run the frontend

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

### Download local AI models

```bash
ollama pull qwen3:1.7b
ollama pull all-minilm
```

The backend will be available at:

`http://localhost:8000`

API documentation:

`http://localhost:8000/docs`

The frontend will be available at:

`http://localhost:5173`

## Development Status

**Currently under active development.**

| Component | Status |
|---|---|
| Backend setup | Completed |
| PDF ingestion | Implemented |
| Text chunking | Implemented |
| Embedding generation | Implemented |
| Vector storage | Implemented |
| Hybrid retrieval | Initial implementation |
| RAG response generation | Initial implementation |
| Citation verification | Planned |
| Frontend integration | In progress |
| RAG evaluation framework | Planned |

## Future Improvements

- Advanced hybrid retrieval and reranking
- Improved citation accuracy and verification
- Multi-document analysis
- RFP requirement extraction
- Automated requirement-to-capability mapping
- Gap analysis
- Interactive analytics dashboard
- RAG evaluation and benchmarking
- Docker-based deployment

## Project Goal

Build a practical, open-source enterprise AI application that demonstrates the integration of Retrieval-Augmented Generation, local language models, intelligent document retrieval, and full-stack development.

---

**Repository:** https://github.com/Sanskruti-Gohil/RFPilot