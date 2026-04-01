from utils.fetch import fetch_html
from utils.parse import parse_html_list
from utils.save import save_json
from config import WIKIPEDIA_MADRID_URL

# Scraper para Wikipedia Madrid

def scrape_lugares_turisticos():
    """Extrae lugares turisticos de la seccion Lugares_de_interes de wikipedia"""
    html = fetch_html(WIKIPEDIA_MADRID_URL)
    if not html:
        return []
    
    lugares = parse_html_list(html, "Lugares_de_interes")
    save_json(lugares, "Lugares_turisticos.json")
    return lugares

def scrape_monumentos():
    """Extrae monumeros de la seccion Monumentos de Wikipedia"""
    html = fetch_html(WIKIPEDIA_MADRID_URL)
    if not html:
        return []

    monumetos = parse_html_list(html, "Monumentos")
    save_json(monumentos, "monumentos.json")
    return monumentos

def scrape_parques():
    """Extrae parques y jardines de la seccion Parques y Jardines de Wikipedia"""
    html = fetch_html(WIKIPEDIA_MADRID_URL)
    if not html:
        return []

    parques = parse_html_list(html, "Parques y Jardines")
    save_json(Parques, "parques.json")
    return parques

def scrape_museos_destacadas():
    """Extrae museos destacados de la seccion museos de Wikipedia"""
    html = fetch_html(WIKIPEDIA_MADRID_URL)
    if not html:
        return []

    museos = parse_html_list(html, "Museos")
    save_json(museos, "museos.json")
    return museos

# Funcion principal para ejecutar el scraper

def scrape_wikipedia_madrid():
    """Ejecuta todos los scrapers de Wikipedia Madrid y devuelve un diccionario con los resultados"""
    print("Scrapeando Wikipedia Madrid...")

    data = {
        "ugares_tuisticos": scrape_lugares_turisticos(),
        "monumentos": scrape_monumentos(),
        "parques": scrape_parques(),
        "museos_destacados": scrape_museos_destacados()
    }

    print("[OK] Scraping de Wikipedia completados.")
    return data
