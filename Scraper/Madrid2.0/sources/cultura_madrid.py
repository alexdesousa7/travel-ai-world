import requests
from bs4 import BeautifulSoup
import json
import os

WIKI_API = "https://es.wikipedia.org/api/rest_v1/page/html/Madrid"


def get_cultura_madrid(output_path="data/cultura_madrid.json"):
    print(">> Cultura de Madrid - Wikipedia REST API…")

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
    capture = False
    current_title = "Cultura"
    current_text = []

    for elem in soup.find_all(["h2", "p"]):

        # Detectar el H2 "Cultura"
        if elem.name == "h2":
            title = elem.get_text(strip=True)

            # Si encontramos "Cultura", empezamos a capturar
            if "Cultura" in title:
                capture = True
                continue

            # Si ya estábamos capturando y llega otro h2 → fin de la sección
            if capture:
                break

        # Capturar párrafos
        if capture and elem.name == "p":
            txt = elem.get_text(strip=True)
            if txt:
                current_text.append(txt)

    # Guardar sección
    sections.append({
        "title": current_title,
        "summary": " ".join(current_text).strip(),
        "source": "Wikipedia REST API"
    })

    os.makedirs("data", exist_ok=True)

    final = {
        "city": "Madrid",
        "category": "cultura",
        "sections": sections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4, ensure_ascii=False)

    print(f">> Cultura de Madrid guardada. Secciones: {len(sections)}")
    return final
