import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi.responses import FileResponse
import os


def export_to_csv(test_cases, file_path="exports/test_cases.csv"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Title", "Description", "Type", "Steps", "Expected Result"])
        for tc in test_cases:
            writer.writerow([
                tc["title"],
                tc["description"],
                tc["type"],
                " | ".join(tc["steps"]),
                tc["expected"],
            ])
    return file_path


def export_to_pdf(test_cases, file_path="exports/test_cases.pdf"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    y = height - 50
    for i, tc in enumerate(test_cases, 1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"{i}. {tc['title']}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"Description: {tc['description']}")
        y -= 15
        c.drawString(60, y, f"Type: {tc['type']}")
        y -= 15
        c.drawString(60, y, f"Steps: {' | '.join(tc['steps'])}")
        y -= 15
        c.drawString(60, y, f"Expected: {tc['expected']}")
        y -= 30
        if y < 100:
            c.showPage()
            y = height - 50
    c.save()
    return file_path
