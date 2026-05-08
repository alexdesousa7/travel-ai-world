from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import BARES_MADRID_URL as URL

def parse_bares(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    bar_cards = soup.select(".bar-card, .list-item, article, .result")

    for card in bar_cards:
        name_el = card.select_one(".name, h2, h3, .title")
        address_el = card.select_one(".address, .location")
        desc_el = card.select_one(".description, p")
        url_el = card.select_one("a")

        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue

        address = address_el.get_text(strip=True) if address_el else None
        description = desc_el.get_text(strip=True) if desc_el else None
        url = url_el["href"] if url_el and url_el.has_attr("href") else None

        item = {
            "name": name,
            "address": address,
            "description": description,
            "url": url,
            "category": "bar",
            "city": "Madrid",
            "source": URL
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "bar",
        "count": len(items),
        "items": items,
        "source": URL
    }


def scrape_bares_madrid():
    html = fetch_html(URL)
    data = parse_bares(html)
    save_json(data, "bares_madrid.json")
    return data


if __name__ == "__main__":
    scrape_bares_madrid()
