from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import ESTADIOS_MADRID_URL as URL

def parse_estadios(html):
    soup = BeautifulSoup(html, "lxml")
    items = []

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
        "categoria": "estadios_madrid",
        "total": len(items),
        "items": items,
        "fuente": URL
    }

def scrape_estadios_madrid():
    html = fetch_html(URL)
    data = parse_estadios(html)
    save_json(data, "estadios_madrid.json")
    return data
