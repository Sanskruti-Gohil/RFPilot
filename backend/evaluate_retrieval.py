
from rank_bm25 import BM25Okapi
from app.services.vector_store import collection
from app.services.embeddings import generate_embeddings
from app.services.retrieval import tokenize

questions = [
    "Does Northstar Digital Services have ISO 27001 certification?",
    "Where is Northstar Digital Services headquartered?",
    "What is Northstar Digital Services' annual revenue?",
    "How does Northstar protect data during transmission?"
]

stored = collection.get(
    include=["documents", "metadatas"]
)

documents = stored["documents"] or []
metadatas = stored["metadatas"] or []

if not documents:
    print("No documents found.")
    raise SystemExit

tokenized_docs = [tokenize(doc) for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

for question in questions:
    print("\n" + "=" * 75)
    print("QUESTION:", question)
    print("=" * 75)

    # Semantic search
    query_embedding = generate_embeddings([question])[0]

    semantic = collection.query(
        query_embeddings=[query_embedding],
        n_results=len(documents),
        include=["distances"]
    )

    semantic_distances = dict(
        zip(semantic["ids"][0], semantic["distances"][0])
    )

    # BM25 search
    bm25_scores = bm25.get_scores(tokenize(question))

    print("\n--- RANKED CHUNKS ---")

    for i, (doc_id, document, metadata) in enumerate(
        zip(stored["ids"], documents, metadatas)
    ):
        print("\nDocument:", metadata["filename"])
        print("Page:", metadata["page_number"])
        print("Semantic distance:", round(
            semantic_distances.get(doc_id, 999), 4
        ))
        print("BM25 score:", round(float(bm25_scores[i]), 4))
        print("Content:", document[:250].replace("\n", " "))
