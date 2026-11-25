
from app.services.reranker import rerank_chunks

tests = [
    {
    "question": (
        "How does Northstar protect data during transmission? "
        "HTTPS TLS encryption data transferred company-managed web applications"
    ),
    "expected": "HTTPS with TLS 1.2 or later"
},
    {
        "question": "Where is Northstar headquartered?",
        "expected": "Pune, Maharashtra, India"
    },
    {
        "question": "Does Northstar have ISO 27001 certification?",
        "expected": "does not hold ISO 27001"
    }
]

chunks = [
    {
        "text": "Data transferred through company-managed web applications must use HTTPS with TLS 1.2 or later.",
        "filename": "security_policy.pdf",
        "page_number": 1
    },
    {
        "text": "Northstar Digital Services does not hold ISO 27001 or SOC 2 certification.",
        "filename": "company_profile.pdf",
        "page_number": 1
    },
    {
        "text": "Northstar is headquartered in Pune, Maharashtra, India.",
        "filename": "company_profile.pdf",
        "page_number": 1
    }
]

for test in tests:
    print("\nQUESTION:", test["question"])

    results = rerank_chunks(
        test["question"],
        chunks,
        top_k=3
    )

    for rank, result in enumerate(results, start=1):
        print(
            rank,
            round(result["rerank_score"], 4),
            result["text"]
        )
