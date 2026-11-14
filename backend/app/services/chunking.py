
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text):

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + CHUNK_SIZE, len(text))

        if end < len(text):
            split_at = text.rfind(" ", start, end)

            if split_at > start + int(CHUNK_SIZE * 0.6):
                end = split_at

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks
