from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import RUTAS_MADRID_URL as URL

def parse_routes(html):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # Cada ruta aparece como tarjeta dentro de .views-row
    cards = soup.select(".views-row")

    for card in cards:
        title = card.select_one(".title a")
        desc = card.select_one(".field-content p")
        link = title["href"] if title else None

        items.append({
            "nombre": title.get_text(strip=True) if title else None,
            "descripcion": desc.get_text(strip=True) if desc else None,
            "url": f"https://www.esmadrid.com{link}" if link else None
        })

    return {
        "categoria": "rutas_turisticas_madrid",
        "total": len(items),
        "items": items,
        "fuente": URL
    }

def scrape_rutas_madrid():
    html = fetch_html(URL)
    data = parse_routes(html)
    save_json(data, "rutas_madrid.json")
    return data
