
import re
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP



def split_into_sections(text):

    pattern = r"(?m)(?=^\s*\d+\.\s+[A-Z])"

    matches = list(re.finditer(pattern, text))

    if not matches:
        return [text.strip()] if text.strip() else []

    sections = []

    # Keep the document header with the first section
    header = text[:matches[0].start()].strip()

    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if i == 0 and header:
            section = header + "\n" + section

        if section:
            sections.append(section)

    return sections


def chunk_text(text):

    sections = split_into_sections(text)
    chunks = []

    for section in sections:

        start = 0

        while start < len(section):

            end = min(start + CHUNK_SIZE, len(section))

            if end < len(section):
                split_at = section.rfind(" ", start, end)

                if split_at > start + int(CHUNK_SIZE * 0.6):
                    end = split_at

            chunk = section[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(section):
                break

            start = end - CHUNK_OVERLAP

    return chunks
