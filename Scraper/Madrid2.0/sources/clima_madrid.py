import requests
from bs4 import BeautifulSoup
import json
import os

WIKI_API = "https://es.wikipedia.org/api/rest_v1/page/html/Clima_de_Madrid"


def get_clima_madrid(output_path="data/clima_madrid.json"):
    print(">> Clima de Madrid - Wikipedia REST API…")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html"
    }

    r = requests.get(WIKI_API, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    sections = []
    current_title = None
    current_text = []

    for elem in soup.find_all(["h2", "p"]):
        if elem.name == "h2":
            if current_title and current_text:
                sections.append({
                    "title": current_title,
                    "summary": " ".join(current_text).strip(),
                    "source": "Wikipedia REST API"
                })
                current_text = []

            current_title = elem.get_text(strip=True)

        elif elem.name == "p":
            txt = elem.get_text(strip=True)
            if txt:
                current_text.append(txt)

    if current_title and current_text:
        sections.append({
            "title": current_title,
            "summary": " ".join(current_text).strip(),
            "source": "Wikipedia REST API"
        })

    os.makedirs("data", exist_ok=True)

    final = {
        "city": "Madrid",
        "category": "clima",
        "sections": sections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4, ensure_ascii=False)

    print(f">> Clima de Madrid guardado. Secciones: {len(sections)}")
    return final
