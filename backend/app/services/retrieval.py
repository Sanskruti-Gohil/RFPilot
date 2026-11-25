
import re

from rank_bm25 import BM25Okapi

from app.services.vector_store import collection
from app.services.embeddings import generate_embeddings
from app.services.reranker import rerank_chunks


def tokenize(text):
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def expand_query(question):
    expanded = question.lower()

    expansions = {
        "transmission": "data transferred",
        "protect": "HTTPS TLS encryption",
        "security": "HTTPS TLS encryption",
    }

    for term, related_terms in expansions.items():
        if term in expanded:
            expanded += " " + related_terms

    return expanded


def retrieve_chunks(question, document_id=None, top_k=5):

    filters = None

    if document_id:
        filters = {"document_id": document_id}

    get_args = {"include": ["documents", "metadatas"]}

    if filters:
        get_args["where"] = filters

    stored = collection.get(**get_args)

    documents = stored["documents"] or []
    metadatas = stored["metadatas"] or []
    ids = stored["ids"]

    if not documents:
        return []

    # Expand query for retrieval
    search_query = expand_query(question)

    # Semantic search
    query_embedding = generate_embeddings([search_query])[0]

    semantic_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(5, len(documents)),
        where=filters,
        include=["distances"]
    )

    semantic_ids = semantic_results["ids"][0]

    # BM25 keyword search
    tokenized_docs = [tokenize(doc) for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)

    scores = bm25.get_scores(tokenize(search_query))
    score_map = dict(zip(ids, scores))

    keyword_ids = sorted(
        [chunk_id for chunk_id in ids if score_map[chunk_id] > 0],
        key=lambda chunk_id: score_map[chunk_id],
        reverse=True
    )[:5]

    # Reciprocal Rank Fusion
    rrf_scores = {}

    for rank, chunk_id in enumerate(semantic_ids, start=1):
        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0) + 1 / (60 + rank)
        )

    for rank, chunk_id in enumerate(keyword_ids, start=1):
        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0) + 1 / (60 + rank)
        )

    ranked_ids = sorted(
        rrf_scores,
        key=rrf_scores.get,
        reverse=True
    )

    document_map = dict(zip(ids, documents))
    metadata_map = dict(zip(ids, metadatas))

    candidates = []
    seen_texts = set()

    for chunk_id in ranked_ids:

        text = document_map[chunk_id]
        normalized_text = " ".join(text.lower().split())

        if normalized_text in seen_texts:
            continue

        seen_texts.add(normalized_text)

        metadata = metadata_map[chunk_id]

        candidates.append({
            "text": text,
            "filename": metadata["filename"],
            "page_number": metadata["page_number"],
            "chunk_id": chunk_id,
            "retrieval_score": round(rrf_scores[chunk_id], 5)
        })

    # Cross-encoder reranking
    reranked_chunks = rerank_chunks(
        search_query,
        candidates,
        top_k=top_k
    )

    print("\n--- RERANKING RESULTS ---")

    for chunk in reranked_chunks:
        print(
            "Rerank score:", round(chunk["rerank_score"], 4),
            "| File:", chunk["filename"],
            "| Content:", chunk["text"][:100]
        )

    print("\n--- RERANKING RESULTS ---")

    for chunk in reranked_chunks:
        print(
            "Score:", round(chunk["rerank_score"], 4),
            "| File:", chunk["filename"],
            "| Chunk:", chunk["chunk_id"]
        )



    return reranked_chunks
