from flask import Flask, render_template
from sanity import Client

app = Flask(__name__)

client = Client({
    "projectId": "YOUR_PROJECT_ID",
    "dataset": "production",
    "useCdn": False
})

def get_content():
    return client.fetch('*[_type == "content"][0]')

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
