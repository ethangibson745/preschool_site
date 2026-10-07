from flask import Flask, render_template
from sanity_client import fetch_content, build_image_url

app = Flask(__name__)

@app.route("/")
def home():
    content = fetch_content()

    home_image_url = build_image_url(content.get("home_image"))
    
    return render_template(
        "home.html",
        home_title=content.get("home_title"),
        home_paragraph=content.get("home_paragraph"),
        home_image=home_image_url
    )


@app.route("/about")
def about():
    content = fetch_content()
    return render_template(
        "about.html",
        about_title=content.get("about_title"),
        about_paragraph=content.get("about_paragraph")
    )

@app.route("/curriculum")
def curriculum():
    content = fetch_content()
    return render_template(
        "curriculum.html",
        curriculum_title=content.get("curriculum_title"),
        curriculum_paragraph=content.get("curriculum_paragraph")
    )

@app.route("/gallery")
def gallery():
    content = fetch_content()

    gallery_urls = [
        build_image_url(img) for img in content.get("gallery_images", [])
    ]

    return render_template(
        "gallery.html",
        gallery_title=content.get("gallery_title"),
        gallery_images=gallery_urls
    )

@app.route("/contact")
def contact():
    content = fetch_content()
    return render_template(
        "contact.html",
        contact_title=content.get("contact_title"),
        contact_email=content.get("contact_email"),
        contact_phone=content.get("contact_phone"),
        contact_address=content.get("contact_address")
    )

if __name__ == "__main__":
    app.run(debug=True)
