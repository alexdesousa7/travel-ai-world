from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import HOSPITALES_MADRID_URL, CENTROS_SANITARIOS_FALLBACK_URL

def parse_centros(html):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # Cada centro aparece como tarjeta dentro de .views-row
    cards = soup.select(".views-row")

    for card in cards:
        title = card.select_one("h2.node__title a")
        tipo = card.select_one(".field--name-field-tipo-centro .field__item")
        direccion = card.select_one(".field--name-field-direccion .field__item")
        telefono = card.select_one(".field--name-field-telefono .field__item")
        desc = card.select_one(".field--name-body p")

        link = title["href"] if title else None

        items.append({
            "nombre": title.get_text(strip=True) if title else None,
            "tipo": tipo.get_text(strip=True) if tipo else None,
            "descripcion": desc.get_text(strip=True) if desc else None,
            "direccion": direccion.get_text(strip=True) if direccion else None,
            "telefono": telefono.get_text(strip=True) if telefono else None,
            "url": f"https://www.comunidad.madrid{link}" if link else None
        })

    return items

def scrape_hospitales_madrid():
    # 1. Intentar solo hospitales
    html = fetch_html(HOSPITALES_MADRID_URL)

    if html is None:
        print("[WARN] URL de hospitales falló. Usando fallback general…")
        html = fetch_html(CENTROS_SANITARIOS_FALLBACK_URL)

    items = parse_centros(html)

    data = {
        "categoria": "centros_sanitarios_madrid",
        "total": len(items),
        "items": items,
        "fuente": HOSPITALES_MADRID_URL
    }

    save_json(data, "hospitales_madrid.json")
    return data
