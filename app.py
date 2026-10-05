from io import BytesIO

from flask import Flask, render_template, request, send_file
from xhtml2pdf import pisa

app = Flask(__name__)


def collect(form, prefix, fields):
    """Zip repeated form fields (e.g. edu_degree[], edu_school[]) into a list of dicts,
    skipping entries where every field is empty."""
    columns = [form.getlist(f"{prefix}_{f}[]") for f in fields]
    items = []
    for values in zip(*columns):
        values = [v.strip() for v in values]
        if any(values):
            items.append(dict(zip(fields, values)))
    return items


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    f = request.form
    data = {
        "name": f.get("name", "").strip(),
        "email": f.get("email", "").strip(),
        "phone": f.get("phone", "").strip(),
        "location": f.get("location", "").strip(),
        "links": f.get("links", "").strip(),
        "summary": f.get("summary", "").strip(),
        "skills": [s.strip() for s in f.get("skills", "").split(",") if s.strip()],
        "education": collect(f, "edu", ["degree", "school", "period", "note"]),
        "projects": collect(f, "proj", ["title", "tech", "desc"]),
        "experience": collect(f, "exp", ["role", "org", "period", "desc"]),
    }

    html = render_template("resume.html", **data)
    buffer = BytesIO()
    result = pisa.CreatePDF(html, dest=buffer)
    if result.err:
        return "Could not create the PDF. Please check your input and try again.", 500

    buffer.seek(0)
    filename = (data["name"] or "resume").replace(" ", "_") + "_resume.pdf"
    return send_file(buffer, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
