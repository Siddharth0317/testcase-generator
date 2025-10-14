from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.nlp_engine import get_engine

app = FastAPI(title="TestCase Generator API")
engine = get_engine()

class ReqIn(BaseModel):
    requirement: str

class TestCaseOut(BaseModel):
    title: str
    description: str
    type: str
    steps: List[str]
    expected: str

@app.post("/generate", response_model=List[TestCaseOut])
def generate(req: ReqIn):
    return engine.generate_test_cases(req.requirement)

@app.get("/health")
def health():
    return {"status": "ok"}
