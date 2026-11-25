
from app.services.evidence_validation import verify_evidence


# Test evidence: Northstar security policy
encryption_chunk = {
    "filename": "02_northstar_security_and_data_policy.pdf",
    "page_number": 1,
    "text": """
    Encryption and Backups

    Company-managed web applications must use HTTPS with
    TLS 1.2 or higher to protect data during transmission.
    """
}

# Test evidence: Northstar company profile
company_chunk = {
    "filename": "01_northstar_company_profile.pdf",
    "page_number": 1,
    "text": """
    Company Overview

    Northstar Digital Services is headquartered in Pune,
    Maharashtra, India. The company has 42 employees.
    """
}


tests = [
    {
        "question": "Where is Northstar headquartered?",
        "chunks": [company_chunk],
        "expected": "SUPPORTED"
    },
    {
        "question": "How does Northstar protect data during transmission?",
        "chunks": [encryption_chunk],
        "expected": "SUPPORTED"
    },
    {
        "question": "What is Northstar's annual revenue?",
        "chunks": [company_chunk],
        "expected": "NOT_FOUND"
    }
]


for test in tests:

    print("\nQuestion:", test["question"])

    result = verify_evidence(
        test["question"],
        test["chunks"]
    )

    print("Expected:", test["expected"])
    print("Actual:", result["status"])
    print("Reason:", result["reason"])

    if result["status"] == test["expected"]:
        print("Result: PASS")
    else:
        print("Result: FAIL")
    
    print("-" * 50)
