import spacy
from typing import List, Dict

class NLPTestEngine:
    """Simple test case generator using spaCy blank model (no training)."""

    def __init__(self):
        # Use a blank English model
        self.nlp = spacy.blank("en")

    def generate_test_cases(self, requirement: str) -> List[Dict]:
        # Dummy prediction: classify by keyword
        category = "functional" if any(
            kw in requirement.lower() for kw in ["login", "upload", "register", "reset", "search"]
        ) else "nonfunctional"

        tests = []

        tc = {
            "title": f"Test: {requirement[:60]}",
            "description": requirement,
            "type": category,
            "steps": [],
            "expected": "",
        }

        # Add steps & expected based on simple keywords
        if "login" in requirement.lower():
            tc["steps"] = ["Open login page", "Enter valid credentials", "Click Login"]
            tc["expected"] = "User is logged in successfully"
        elif "upload" in requirement.lower():
            tc["steps"] = ["Open upload dialog", "Select file", "Click Upload"]
            tc["expected"] = "File is uploaded successfully"
        else:
            tc["steps"] = ["Perform the action described in requirement"]
            tc["expected"] = "System behaves as expected"

        tests.append(tc)

        # Add an edge case
        edge = tc.copy()
        edge["title"] = tc["title"] + " - Edge Case"
        edge["steps"] = ["Provide invalid input", "Submit"]
        edge["expected"] = "Proper validation/error handling"
        tests.append(edge)

        return tests


# Global engine instance
_engine: NLPTestEngine | None = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = NLPTestEngine()
    return _engine
