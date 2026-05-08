from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import CENTROS_COMERCIALES_MADRID_URL as URL

def parse_centros(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []

    rows = soup.select("table tr")

    for row in rows:
        cols = row.select("td")
        if len(cols) < 2:
            continue

        name = cols[0].get_text(strip=True)
        location = cols[1].get_text(strip=True)
        year = cols[2].get_text(strip=True) if len(cols) > 2 else None

        item = {
            "name": name,
            "location": location,
            "year_opened": year,
            "category": "shopping_center",
            "city": "Madrid",
            "source": URL
        }

        items.append(item)

    return {
        "city": "Madrid",
        "category": "shopping_center",
        "count": len(items),
        "items": items,
        "source": URL
    }


def scrape_centros_comerciales_madrid():
    html = fetch_html(URL)
    data = parse_centros(html)
    save_json(data, "centros_comerciales_madrid.json")
    return data


if __name__ == "__main__":
    scrape_centros_comerciales_madrid()
