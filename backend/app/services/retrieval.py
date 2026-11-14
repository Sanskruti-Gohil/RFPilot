
from rank_bm25 import BM25Okapi

from app.services.vector_store import collection
from app.services.embeddings import generate_embeddings


def retrieve_chunks(question, document_id=None, top_k=5):

    # Get stored documents
    filters = None

    if document_id:
        filters = {"document_id": document_id}

    stored = collection.get(
        where=filters,
        include=["documents", "metadatas"]
    )

    documents = stored["documents"]
    metadatas = stored["metadatas"]
    ids = stored["ids"]

    if not documents:
        return []

    # -------------------------
    # 1. Semantic Search
    # -------------------------

    query_embedding = generate_embeddings([question])[0]

    search_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, len(documents)),
        where=filters,
        include=["documents", "metadatas", "distances"]
    )

    semantic_ids = search_results["ids"][0]

    # -------------------------
    # 2. BM25 Keyword Search
    # -------------------------

    tokenized_docs = [
        doc.lower().split() for doc in documents
    ]

    bm25 = BM25Okapi(tokenized_docs)

    tokenized_question = question.lower().split()

    scores = bm25.get_scores(tokenized_question)

    keyword_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    keyword_ids = [
        ids[i] for i in keyword_indices
    ]

    # -------------------------
    # 3. Reciprocal Rank Fusion
    # -------------------------

    rrf_scores = {}

    for rank, chunk_id in enumerate(semantic_ids):
        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0) + 1 / (60 + rank + 1)
        )

    for rank, chunk_id in enumerate(keyword_ids):
        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0) + 1 / (60 + rank + 1)
        )

    ranked_ids = sorted(
        rrf_scores,
        key=rrf_scores.get,
        reverse=True
    )[:top_k]

    # -------------------------
    # 4. Return Retrieved Chunks
    # -------------------------

    metadata_map = dict(zip(ids, metadatas))
    document_map = dict(zip(ids, documents))

    results = []

    for chunk_id in ranked_ids:

        results.append({
            "text": document_map[chunk_id],
            "filename": metadata_map[chunk_id]["filename"],
            "page_number": metadata_map[chunk_id]["page_number"],
            "chunk_id": chunk_id,
            "retrieval_score": round(
                rrf_scores[chunk_id], 5
            )
        })

    return results
