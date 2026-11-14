
import chromadb
import uuid

from app.core.config import VECTOR_DIR


client = chromadb.PersistentClient(
    path=str(VECTOR_DIR)
)

collection = client.get_or_create_collection(
    name="rfpilot_documents",
    metadata={"hnsw:space": "cosine"},
    embedding_function=None
)


def store_chunks(chunks, embeddings, document_id, filename):

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(str(uuid.uuid4()))

        documents.append(chunk["text"])

        metadatas.append({
            "document_id": document_id,
            "filename": filename,
            "page_number": chunk["page_number"],
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)
