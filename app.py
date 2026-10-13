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

@app.route("/")
def home():
    data = get_content()
    return render_template(
        "home.html",
        home_title=data.get("home_title", ""),
        home_paragraph=data.get("home_paragraph", ""),
        home_image=data.get("home_image", "")
    )
