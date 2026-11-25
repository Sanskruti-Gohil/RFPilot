
import ollama

from app.core.config import LLM_MODEL


def generate_answer(question, context):

    if not context:
        return (
            "I could not find relevant information "
            "in the uploaded documents."
        )

    context_text = ""

    for index, chunk in enumerate(context, start=1):

        context_text += f"""
Source {index}:
Document: {chunk['filename']}
Page: {chunk['page_number']}

Content:
{chunk['text']}

"""

    prompt = f"""
You are RFPilot, an enterprise document intelligence assistant.

Answer the user's question using ONLY the supplied document context.

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. If the context does not contain the answer, clearly say so.
4. Keep answers concise and professional.
5. Cite only sources that directly support your answer.
6. Do not cite irrelevant sources.
7. Never infer missing business information.
8. Distinguish confirmed information from unavailable information.

DOCUMENT CONTEXT:

{context_text}

USER QUESTION:

{question}

Provide a concise, evidence-based answer.

 /no_think
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1,
            "num_ctx": 2048,
            "num_predict": 350
        }
    )

    return response.message.content
