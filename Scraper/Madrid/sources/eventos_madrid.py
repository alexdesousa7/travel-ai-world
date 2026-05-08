from utils.fetch import fetch_json
from utils.save import save_json
from config import EVENTOS_ENDPOINT

def scrape_eventos_madrid():
    data = fetch_json(EVENTOS_ENDPOINT)
    if data:
        save_json(data, "eventos_madrid.json")
    return data

if __name__ == "__main__":
    scrape_eventos_madrid()
