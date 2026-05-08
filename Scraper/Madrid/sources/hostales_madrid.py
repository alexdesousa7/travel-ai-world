from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import HOSTALES_MADRID_URL as URL

def parse_hostels(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # TODO: ajusta estos selectores según la estructura real de la página
    hostel_cards = soup.select(".hostel-card, .list-item, article, .result")

    for card in hostel_cards:
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
            "category": "hostel",
            "city": "Madrid",
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "hostel",
        "count": len(items),
        "items": items,
        "source": URL,
    }


def scrape_hostales_madrid():
    html = fetch_html(URL)
    data = parse_hostels(html)
    save_json(data, "hostales_madrid.json")
    return data


if __name__ == "__main__":
    scrape_hostales_madrid()
