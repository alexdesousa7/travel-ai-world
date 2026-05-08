from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import BARRIOS_MADRID_URL as URL


def parse_neighborhoods(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    # TODO: ajusta estos selectores según la estructura real de la página
    barrio_rows = soup.select("table tr, .barrio-card, .list-item, article")

    for row in barrio_rows:
        name_el = row.select_one(".name, h2, h3, .title, td:nth-child(1)")
        district_el = row.select_one(".district, .distrito, td:nth-child(2)")
        desc_el = row.select_one(".description, p")
        url_el = row.select_one("a")

        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue

        district = district_el.get_text(strip=True) if district_el else None
        description = desc_el.get_text(strip=True) if desc_el else None
        url = url_el["href"] if url_el and url_el.has_attr("href") else None

        item = {
            "name": name,
            "district": district,
            "description": description,
            "url": url,
            "source": URL,
            "category": "neighborhood",
            "city": "Madrid",
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "neighborhood",
        "count": len(items),
        "items": items,
        "source": URL,
    }


def scrape_barrios_madrid():
    html = fetch_html(URL)
    data = parse_neighborhoods(html)
    save_json(data, "barrios_madrid.json")
    return data


if __name__ == "__main__":
    scrape_barrios_madrid()
