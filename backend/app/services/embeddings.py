
import ollama

from app.core.config import EMBEDDING_MODEL


def generate_embeddings(texts):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return response.embeddings
