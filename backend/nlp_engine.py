# backend/nlp_engine.py
import spacy
from typing import List, Dict

# Load trained spaCy model
nlp = spacy.load("models/testgen_model")

def generate_test_cases(requirement: str) -> List[Dict]:
    doc = nlp(requirement)
    # Choose category with highest probability
    category = max(doc.cats, key=doc.cats.get)

    return [{
        "title": f"Test: {requirement[:50]}",
        "description": requirement,
        "type": category,
        "steps": [
            "Perform the actions described in requirement",
            "Verify expected system behavior"
        ],
        "expected": "System behaves as expected"
    }]
