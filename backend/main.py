# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from backend.nlp_engine import generate_test_cases
from fastapi.responses import Response
import json

app = FastAPI()

class Requirement(BaseModel):
    requirement: str

@app.post("/generate")
def generate(req: Requirement) -> List[Dict]:
    return generate_test_cases(req.requirement)

@app.post("/generate_selenium")
def selenium_export(test_cases: list):
    """
    Accepts a list of test cases and returns a Selenium Python script.
    """
    file_path = generate_selenium_script(test_cases)
    return FileResponse(file_path, media_type="text/x-python", filename="selenium_test_cases.py")

@app.post("/export/pdf")
def export_pdf(tests: List[Dict]):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Generated Test Cases", ln=True, align="C")
    pdf.set_font("Arial", "", 12)

    for t in tests:
        pdf.ln(5)
        pdf.multi_cell(0, 8, f"Title: {t['title']}")
        pdf.multi_cell(0, 8, f"Type: {t['type']}")
        pdf.multi_cell(0, 8, f"Description: {t['description']}")
        pdf.multi_cell(0, 8, f"Steps:")
        for s in t['steps']:
            pdf.multi_cell(0, 8, f" - {s}")
        pdf.multi_cell(0, 8, f"Expected Outcome: {t['expected']}")
        pdf.ln(5)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return Response(pdf_output, media_type="application/pdf")
