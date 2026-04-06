from utils.fetch import fetch_html
from utils.save import save_json
from config import WIKIPEDIA_MADRID_URL
from bs4 import BeautifulSoup


# Funciones de bsuqueda robustas en el HTML para extraer secciones especificas, debido a que del otro modo no extrae la informacion correctamente.


def extract_section(html, keywords):
    keywords = [k.lower() for k in keywords]

    for h in html.find_all(["h2", "h3"]):
        title = h.get_text().strip().lower()

        if any(k in title for k in keywords):
            content = []
            node = h.find_next_sibling()

            while node and node.name not in ["h2", "h3"]:
                if node.name == "p":
                    content.append(node.get_text(strip=True))

                if node.name == "ul":
                    items = [li.get_text(strip=True) for li in node.find_all("li")]
                    content.extend(items)

                node = node.find_next_sibling()

            return content

    return []


def extract_list(html, keywords):
    keywords = [k.lower() for k in keywords]

    for h in html.find_all(["h2", "h3"]):
        title = h.get_text().strip().lower()

        if any(k in title for k in keywords):
            ul = h.find_next("ul")
            if ul:
                return [li.get_text(strip=True) for li in ul.find_all("li")]

    return []



# Scrapers específicos a extraer de secciones en concreto de la Wikipedia de Madrid.


def scrape_lugares_turisticos(html):
    return extract_section(html, ["patrimonio", "lugares", "interés"])


def scrape_monumentos(html):
    return extract_section(html, ["patrimonio", "monumentos"])


def scrape_museos(html):
    return extract_section(html, ["museos", "galerías"])


def scrape_parques(html):
    return extract_section(html, ["parques", "jardines"])


def scrape_historia(html):
    return extract_section(html, ["historia"])


def scrape_cultura(html):
    return extract_section(html, ["cultura"])


def scrape_gastronomia(html):
    return extract_section(html, ["gastronomía"])



# Función principal para ejecutar el scraper de Wikipedia Madrid.


def scrape_wikipedia_madrid():
    print("Scrapeando Wikipedia Madrid...")

    html_raw = fetch_html(WIKIPEDIA_MADRID_URL)
    if not html_raw:
        print("No se pudo obtener la página de Wikipedia.")
        return {}

    html = BeautifulSoup(html_raw, "lxml")

    data = {
        "lugares_turisticos": scrape_lugares_turisticos(html),
        "monumentos": scrape_monumentos(html),
        "museos": scrape_museos(html),
        "parques": scrape_parques(html),
        "historia": scrape_historia(html),
        "cultura": scrape_cultura(html),
        "gastronomia": scrape_gastronomia(html)
    }

    save_json(data, "wikipedia_madrid.json")

    print("[OK] Scraping de Wikipedia completado.")
    return data
