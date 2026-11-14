
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[2].parent

STORAGE_DIR = PROJECT_ROOT / "storage"
DOCUMENT_DIR = STORAGE_DIR / "documents"
VECTOR_DIR = STORAGE_DIR / "vector_db"

# Create directories if they don't exist
DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

# AI models
LLM_MODEL = "qwen3:1.7b"
EMBEDDING_MODEL = "all-minilm"

# Chunking settings
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

# Upload settings
MAX_FILE_SIZE = 15 * 1024 * 1024
