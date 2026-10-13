import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID")
SANITY_DATASET = os.getenv("SANITY_DATASET")
SANITY_TOKEN = os.getenv("SANITY_TOKEN")

def get_content():
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-10-10/data/query/{SANITY_DATASET}"
    query = '*[_type == "content"][0]'
    params = {"query": query}
    headers = {"Authorization": f"Bearer {SANITY_TOKEN}"}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json().get("result", {}) or {}

def build_image_url(image_obj):
    if not image_obj or "asset" not in image_obj or "_ref" not in image_obj["asset"]:
        return None

    ref = image_obj["asset"]["_ref"]
    parts = ref.split("-")

    file_id = parts[1]
    dimensions = parts[2]
    ext = parts[3]

    return f"https://cdn.sanity.io/images/{SANITY_PROJECT_ID}/{SANITY_DATASET}/{file_id}-{dimensions}.{ext}"

@app.route("/")
def home():
    data = get_content()
    home_image_url = build_image_url(data.get("home_image"))

    return render_template(
        "home.html",
        home_title=data.get("home_title", ""),
        home_paragraph=data.get("home_paragraph", ""),
        home_image=home_image_url
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
    gallery_urls = [
        build_image_url(img) for img in data.get("gallery_images", [])
    ]

    return render_template(
        "gallery.html",
        gallery_title=data.get("gallery_title", ""),
        gallery_images=gallery_urls
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
