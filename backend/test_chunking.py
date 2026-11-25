from app.services.ingestion import extract_pdf

pdf_path = "../storage/documents/186626bb-4fb8-435d-a1ef-457f87905cce.pdf"

chunks = extract_pdf(pdf_path)

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {i} | PAGE {chunk['page_number']} ---")
    print(chunk["text"][:500])