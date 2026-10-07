import requests

PROJECT_ID = "205cf911"
DATASET = "production"

def fetch_content():
    url = f"https://{PROJECT_ID}.api.sanity.io/v2023-10-01/data/query/{DATASET}"

    # FIX: Fetch the newest published content document
    query = '*[_type == "content" && !(_id in path("drafts.**"))] | order(_updatedAt desc)[0]'

    response = requests.get(url, params={"query": query})
    return response.json().get("result", {})

def build_image_url(image_obj):
    if not image_obj or "asset" not in image_obj or "_ref" not in image_obj["asset"]:
        return None

    ref = image_obj["asset"]["_ref"]
    parts = ref.split("-")

    file_id = parts[1]
    dimensions = parts[2]
    file_ext = parts[3]

    return f"https://cdn.sanity.io/images/{PROJECT_ID}/{DATASET}/{file_id}-{dimensions}.{file_ext}"
