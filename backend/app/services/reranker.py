
from sentence_transformers import CrossEncoder


# Load the reranking model
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(
    MODEL_NAME,
    device="cpu"
)


def rerank_chunks(question, chunks, top_k=5):

    if not chunks:
        return []

    # Prepare question and document pairs
    pairs = [
        [question, chunk["text"]]
        for chunk in chunks
    ]

    # Calculate relevance scores
    scores = reranker.predict(
        pairs,
        batch_size=4,
        show_progress_bar=False
    )

    # Attach scores to chunks
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    # Sort by relevance
    ranked_chunks = sorted(
        chunks,
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    return ranked_chunks[:top_k]
