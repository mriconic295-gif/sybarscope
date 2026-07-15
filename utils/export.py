import json, csv, os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

REPORTS_DIR = "reports"

def export_json(data: dict, filename: str):
    os.makedirs(os.path.join(REPORTS_DIR, "json"), exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, "json", f"{filename}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return filepath

def export_csv(data: dict, filename: str):
    os.makedirs(os.path.join(REPORTS_DIR, "csv"), exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, "csv", f"{filename}.csv")
    with open(filepath, "w", newline='') as f:
        writer = csv.writer(f)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key, ", ".join(str(v) for v in value)])
            else:
                writer.writerow([key, str(value)])
    return filepath

def export_pdf(title: str, data: dict, filename: str):
    os.makedirs(os.path.join(REPORTS_DIR, "pdf"), exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, "pdf", f"{filename}.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    for key, value in data.items():
        text = f"{key}: {value}"
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, text)
        y -= 15
    c.save()
    return filepath
