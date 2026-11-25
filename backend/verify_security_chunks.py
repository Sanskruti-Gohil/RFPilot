
from app.services.vector_store import collection

document_id = "8ddf8eab-dbf8-42dd-a7d3-df0748bd213d"

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
    print("Text:", document[:400])
