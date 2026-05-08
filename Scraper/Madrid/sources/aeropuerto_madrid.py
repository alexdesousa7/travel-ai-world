from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import AEROPUERTO_MADRID_URL as URL



def parse_airport(html: str):
    soup = BeautifulSoup(html, "lxml")

    # Título general
    title_el = soup.select_one("h1, .page-title")
    title = title_el.get_text(strip=True) if title_el else "Aeropuerto Adolfo Suárez Madrid-Barajas"

    # Descripción general
    paragraphs = soup.select("p")
    general_info = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 40:
            general_info.append(text)

    # Terminales
    terminal_cards = soup.select(".terminal-card, .terminal, .list-item, article")
    terminals = []

    for card in terminal_cards:
        name_el = card.select_one(".name, h2, h3, .title")
        desc_el = card.select_one(".description, p")

        name = name_el.get_text(strip=True) if name_el else None
        description = desc_el.get_text(strip=True) if desc_el else None

        if name:
            terminals.append({
                "terminal": name,
                "description": description
            })

    # Transporte
    transport_sections = soup.select(".transport, .transporte, h2, h3")
    transport_info = []

    for sec in transport_sections:
        sec_title = sec.get_text(strip=True)
        next_el = sec.find_next_sibling()

        sec_paragraphs = []
        while next_el and next_el.name == "p":
            sec_paragraphs.append(next_el.get_text(strip=True))
            next_el = next_el.find_next_sibling()

        if sec_paragraphs:
            transport_info.append({
                "mode": sec_title,
                "details": sec_paragraphs
            })

    data = {
        "city": "Madrid",
        "category": "airport",
        "name": title,
        "source": URL,
        "summary": general_info[:5],
        "terminals": terminals,
        "transport": transport_info
    }

    return data


def scrape_aeropuerto_madrid():
    html = fetch_html(URL)
    data = parse_airport(html)
    save_json(data, "aeropuerto_madrid.json")
    return data


if __name__ == "__main__":
    scrape_aeropuerto_madrid()
