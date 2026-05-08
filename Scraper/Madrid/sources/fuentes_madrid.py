from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import FUENTES_MADRID_URL as URL

def parse_fountains(html):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # Las páginas de categoría usan este selector
    links = soup.select(".mw-category-group ul li a")

    for link in links:
        nombre = link.get_text(strip=True)
        url = "https://es.wikipedia.org" + link["href"]

        items.append({
            "nombre": nombre,
            "url": url
        })

    return {
        "categoria": "fuentes_madrid",
        "total": len(items),
        "items": items,
        "fuente": URL
    }

def scrape_fuentes_madrid():
    html = fetch_html(URL)
    data = parse_fountains(html)
    save_json(data, "fuentes_madrid.json")
    return data
