from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import TEATROS_MADRID_URL as URL

def parse_teatros(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # TODO: Ajustar selectores según la estructura real de esmadrid.com
    teatro_cards = soup.select(".teatro-card, .list-item, article, .result")

    for card in teatro_cards:
        name_el = card.select_one(".name, h2, h3, .title")
        address_el = card.select_one(".address, .location")
        district_el = card.select_one(".district, .barrio")
        desc_el = card.select_one(".description, p")
        url_el = card.select_one("a")

        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue

        address = address_el.get_text(strip=True) if address_el else None
        district = district_el.get_text(strip=True) if district_el else None
        description = desc_el.get_text(strip=True) if desc_el else None
        url = url_el["href"] if url_el and url_el.has_attr("href") else None

        item = {
            "name": name,
            "address": address,
            "district": district,
            "description": description,
            "url": url,
            "source": URL,
            "category": "theater",
            "city": "Madrid",
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "theater",
        "count": len(items),
        "items": items,
        "source": URL,
    }


def scrape_teatros_madrid():
    html = fetch_html(URL)
    data = parse_teatros(html)
    save_json(data, "teatros_madrid.json")
    return data


if __name__ == "__main__":
    scrape_teatros_madrid()
