from playwright.sync_api import sync_playwright
from utils.save import save_json

URL = "https://www.hoteles.net/madrid/"

def scrape_hoteles_madrid():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded")

        # esperar a que carguen los hoteles
        page.wait_for_selector(".hotel", timeout=10000)

        cards = page.query_selector_all(".hotel")

        hoteles = []

        for card in cards:
            nombre = card.query_selector("h3")
            direccion = card.query_selector(".direccion")
            precio = card.query_selector(".precio")
            imagen = card.query_selector("img")
            enlace = card.query_selector("a")

            hoteles.append({
                "nombre": nombre.inner_text().strip() if nombre else None,
                "direccion": direccion.inner_text().strip() if direccion else None,
                "precio": precio.inner_text().strip() if precio else None,
                "imagen": imagen.get_attribute("src") if imagen else None,
                "url": enlace.get_attribute("href") if enlace else None
            })

        browser.close()

        data = {
            "city": "Madrid",
            "category": "hotel",
            "count": len(hoteles),
            "items": hoteles,
            "source": URL
        }

        save_json(data, "hoteles_madrid.json")
        return data
