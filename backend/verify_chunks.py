
from app.services.vector_store import collection

document_id = "5fe6ff99-c45f-4841-9efc-60333614f3dd"

records = collection.get(
    where={"document_id": document_id},
    include=["documents", "metadatas"]
)

print("Total chunks:", len(records["ids"]))

for i, (document, metadata) in enumerate(
    zip(records["documents"], records["metadatas"]),
    start=1
):
    print(f"\n--- CHUNK {i} ---")
    print("Page:", metadata["page_number"])
    print("Text:", document[:300])
