from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import CITY_CARD_MADRID_URL as URL

def parse_city_card(html):
    soup = BeautifulSoup(html, "lxml")

    # Extraer título principal
    title = soup.select_one("h1")
    intro = soup.select_one(".field--name-body p")

    # Extraer secciones de beneficios o características
    sections = soup.select(".field--name-body ul li")
    beneficios = [li.get_text(strip=True) for li in sections]

    return {
        "categoria": "madrid_city_card",
        "titulo": title.get_text(strip=True) if title else None,
        "descripcion": intro.get_text(strip=True) if intro else None,
        "beneficios": beneficios,
        "fuente": URL
    }

def scrape_city_card_madrid():
    html = fetch_html(URL)
    data = parse_city_card(html)
    save_json(data, "city_card_madrid.json")
    return data
