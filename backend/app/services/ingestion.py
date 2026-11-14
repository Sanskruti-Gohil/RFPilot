
from pypdf import PdfReader

from app.services.chunking import chunk_text


def extract_pdf(file_path):

    reader = PdfReader(file_path)

    all_chunks = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        chunks = chunk_text(text)

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "page_number": page_number
            })

    if not all_chunks:
        raise ValueError(
            "No extractable text found in PDF."
        )

    return all_chunks
