from typing import List

def run_tests(testcases: List[dict]):
    results = []
    for tc in testcases:
        ok = True
        notes = []
        if not tc.get("steps"):
            ok = False
            notes.append("No steps provided")
        if not tc.get("expected"):
            notes.append("No expected outcome provided")
        results.append({"title": tc.get("title"), "passed": ok, "notes": notes})
    return results
