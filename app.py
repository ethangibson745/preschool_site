import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID", "205cf911")
SANITY_DATASET = os.getenv("SANITY_DATASET", "production")
SANITY_TOKEN = os.getenv("SANITY_TOKEN", "YOUR_READ_TOKEN")

def get_content():
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-10-10/data/query/{SANITY_DATASET}"
    query = '*[_type == "content"][0]'
    params = {"query": query}
    headers = {"Authorization": f"Bearer {SANITY_TOKEN}"}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    return result.get("result", {}) or {}

@app.route("/")
def home():
    data = get_content()
    return render_template(
        "home.html",
        home_title=data.get("home_title", ""),
        home_paragraph=data.get("home_paragraph", ""),
        home_image=data.get("home_image", "")
    )

@app.route("/about")
def about():
    data = get_content()
    return render_template(
        "about.html",
        about_title=data.get("about_title", ""),
        about_paragraph=data.get("about_paragraph", "")
    )

@app.route("/curriculum")
def curriculum():
    data = get_content()
    return render_template(
        "curriculum.html",
        curriculum_title=data.get("curriculum_title", ""),
        curriculum_paragraph=data.get("curriculum_paragraph", "")
    )

@app.route("/gallery")
def gallery():
    data = get_content()
    return render_template(
        "gallery.html",
        gallery_title=data.get("gallery_title", ""),
        gallery_images=data.get("gallery_images", [])
    )

@app.route("/contact")
def contact():
    data = get_content()
    return render_template(
        "contact.html",
        contact_title=data.get("contact_title", ""),
        contact_email=data.get("contact_email", ""),
        contact_phone=data.get("contact_phone", ""),
        contact_address=data.get("contact_address", ""),
        contact_extra=data.get("contact_extra", "")
    )

if __name__ == "__main__":
    app.run(debug=True)
