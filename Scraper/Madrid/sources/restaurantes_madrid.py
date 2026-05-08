from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import RESTAURANTES_MADRID_URL as URL



def parse_restaurants(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # TODO: ajusta estos selectores a la estructura real de la página
    restaurant_cards = soup.select(".restaurant-card, .list-item, article")

    for card in restaurant_cards:
        name_el = card.select_one(".name, h2, h3, .title")
        address_el = card.select_one(".address, .location")
        district_el = card.select_one(".district, .barrio")
        desc_el = card.select_one(".description, p")

        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue  # si no hay nombre, no nos sirve

        address = address_el.get_text(strip=True) if address_el else None
        district = district_el.get_text(strip=True) if district_el else None
        description = desc_el.get_text(strip=True) if desc_el else None

        item = {
            "name": name,
            "address": address,
            "district": district,
            "description": description,
            "source": URL,
            "category": "restaurant",
            "city": "Madrid",
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "restaurant",
        "count": len(items),
        "items": items,
        "source": URL,
    }


def scrape_restaurantes_madrid():
    html = fetch_html(URL)
    data = parse_restaurants(html)
    save_json(data, "restaurantes_madrid.json")
    return data


if __name__ == "__main__":
    scrape_restaurantes_madrid()
