from bs4 import BeautifulSoup
from utils.fetch import fetch_html
from utils.save import save_json
from config import INFO_GENERAL_MADRID_URL as URL

def parse_general_info(html: str):
    soup = BeautifulSoup(html, "lxml")

    # TODO: ajusta estos selectores según la estructura real de la página
    title_el = soup.select_one("h1, .page-title")
    paragraphs = soup.select("p")
    sections = soup.select("h2, h3")

    title = title_el.get_text(strip=True) if title_el else "Información general de Madrid"

    # Extraemos texto general
    general_text = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 40:  # evitamos textos muy cortos o basura
            general_text.append(text)

    # Extraemos secciones temáticas
    thematic_sections = []
    for sec in sections:
        sec_title = sec.get_text(strip=True)
        # buscamos párrafos inmediatamente después
        sec_paragraphs = []
        next_el = sec.find_next_sibling()
        while next_el and next_el.name == "p":
            sec_paragraphs.append(next_el.get_text(strip=True))
            next_el = next_el.find_next_sibling()

        if sec_paragraphs:
            thematic_sections.append({
                "section": sec_title,
                "content": sec_paragraphs
            })

    data = {
        "city": "Madrid",
        "category": "general_info",
        "title": title,
        "source": URL,
        "summary": general_text[:5],  # primeros párrafos relevantes
        "sections": thematic_sections
    }

    return data


def scrape_info_general_madrid():
    html = fetch_html(URL)
    data = parse_general_info(html)
    save_json(data, "info_general_madrid.json")
    return data


if __name__ == "__main__":
    scrape_info_general_madrid()
