# Resume Builder

A small Flask app: fill in a form, download a clean one-page resume as a PDF.

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Structure
```
app.py                 routes + PDF generation (xhtml2pdf)
templates/index.html   the form
templates/resume.html  the PDF layout
```

## Ideas to extend
- Multiple resume templates to choose from
- Live preview before download
- Save resumes per user (login + SQLite)
