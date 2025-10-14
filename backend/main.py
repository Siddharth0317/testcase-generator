from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from backend.nlp_engine import get_engine
from backend.export_utils import export_to_csv, export_to_pdf
from backend.test_runner import run_selenium_test
from fastapi.responses import FileResponse

app = FastAPI(title="AI Test Case Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate_test_cases(req: dict = Body(...)):
    requirement = req.get("requirement", "")
    engine = get_engine()
    test_cases = engine.generate_test_cases(requirement)
    return {"test_cases": test_cases}


@app.post("/export/{format}")
def export_test_cases(format: str, req: dict = Body(...)):
    test_cases = req.get("test_cases", [])
    if format == "csv":
        path = export_to_csv(test_cases)
    elif format == "pdf":
        path = export_to_pdf(test_cases)
    else:
        return {"error": "Unsupported format"}
    return FileResponse(path, filename=os.path.basename(path))


@app.post("/run-selenium")
def run_selenium(req: dict = Body(...)):
    url = req.get("url", "https://example.com")
    steps = req.get("steps", [])
    result = run_selenium_test(url, steps)
    return {"status": "completed" if result else "failed"}
