import json, csv, os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# સીધું યુઝરના Downloads ફોલ્ડરમાં 'Sybarscope_Reports' ફોલ્ડર બનાવી દેશે
DOWNLOADS_DIR = os.path.join(Path.home(), "Downloads", "Sybarscope_Reports")

def export_json(data: dict, filename: str):
    json_dir = os.path.join(DOWNLOADS_DIR, "json")
    os.makedirs(json_dir, exist_ok=True)
    filepath = os.path.join(json_dir, f"{filename}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return filepath

def export_csv(data: dict, filename: str):
    csv_dir = os.path.join(DOWNLOADS_DIR, "csv")
    os.makedirs(csv_dir, exist_ok=True)
    filepath = os.path.join(csv_dir, f"{filename}.csv")
    with open(filepath, "w", newline='') as f:
        writer = csv.writer(f)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key, ", ".join(str(v) for v in value)])
            else:
                writer.writerow([key, str(value)])
    return filepath

def export_pdf(title: str, data: dict, filename: str):
    pdf_dir = os.path.join(DOWNLOADS_DIR, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    filepath = os.path.join(pdf_dir, f"{filename}.pdf")
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 40
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    
    for key, value in data.items():
        text = f"{key}: {value}"
        # PDF માં લખાણ કાપાઈ ન જાય તે માટે
        if len(text) > 90:
            text = text[:87] + "..."
        if y < 40:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 10)
        c.drawString(40, y, text)
        y -= 15
        
    c.save()
    return filepath
