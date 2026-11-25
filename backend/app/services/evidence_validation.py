
import json

#from django.template import response
import ollama

from app.core.config import LLM_MODEL

def verify_evidence(question, chunks):

    if not chunks:
        return {
            "status": "NOT_FOUND",
            "verified_chunks": [],
            "reason": "No evidence was retrieved."
        }

    context = []

    for index, chunk in enumerate(chunks, start=1):
        context.append({
            "source_id": index,
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "content": chunk["text"]
        })

    prompt = f"""
You are an evidence verification system for RFPilot.

Determine whether the supplied document sources contain
evidence that answers the user's question.

USER QUESTION:
{question}

DOCUMENT SOURCES:
{json.dumps(context, indent=2)}

Return ONLY valid JSON in this format:

{{
    "status": "SUPPORTED",
    "verified_sources": [1],
    "reason": "The source directly supports the answer."
}}

Rules:
1. SUPPORTED: Evidence directly answers the question.
2. PARTIAL: Evidence answers only part of the question.
3. NOT_FOUND: No source provides relevant evidence.
4. Never use outside knowledge.
5. Do not treat keyword similarity as proof.
6. Do not assume missing information.
7. Include only source IDs that support the verdict.
8. If no source supports the answer, return an empty list.
9. Return exactly one status: SUPPORTED, PARTIAL, or NOT_FOUND.
10. Return JSON only.

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
        format="json",
        options={
            "temperature": 0,
            "num_ctx": 2048,
            "num_predict": 350
        }
    )

    try:
        result = json.loads(response.message.content)

        status = result.get("status")
        valid_statuses = {"SUPPORTED", "PARTIAL", "NOT_FOUND"}

        if status not in valid_statuses:
            raise ValueError("Invalid verification status.")

        source_ids = result.get("verified_sources", [])

        if not isinstance(source_ids, list):
            raise ValueError("Invalid source list.")

        verified_chunks = [
            chunks[source_id - 1]
            for source_id in source_ids
            if isinstance(source_id, int)
            and not isinstance(source_id, bool)
            and 1 <= source_id <= len(chunks)
        ]

        if status == "NOT_FOUND":
            verified_chunks = []

        return {
            "status": status,
            "verified_chunks": verified_chunks,
            "reason": result.get("reason", "")
        }

    except (json.JSONDecodeError, ValueError, TypeError):
        return {
            "status": "NOT_FOUND",
            "verified_chunks": [],
            "reason": "Evidence verification returned an invalid response."
        }