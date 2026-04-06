import requests
from utils.save import save_json


# Datos Abiertos de la Ciudad de Madrid (Funcionales)


URL_MUSEOS = "https://datos.madrid.es/egob/catalogo/201132-0-museos.json"
URL_PARQUES = "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json"


def fetch_json(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error JSON: {url}")
        print(f"Detalle: {e}")
        return None



# Scrapers especificos para cada seccion de Datos Abiertos


def scrape_museos():
    print("Descargando museos...")
    data = fetch_json(URL_MUSEOS)
    if data:
        save_json(data, "museos_madrid.json")
        print("Museos OK")
    return data


def scrape_parques():
    print("Descargando parques...")
    data = fetch_json(URL_PARQUES)
    if data:
        save_json(data, "parques_madrid.json")
        print("Parques OK")
    return data


def scrape_madrid_open_data():
    return {
        "museos": scrape_museos(),
        "parques": scrape_parques()
    }
