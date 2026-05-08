from utils.fetch import fetch_json
from utils.save import save_json
from config import CALIDAD_AIRE_ENDPOINT

def scrape_calidad_aire_madrid():
    data = fetch_json(CALIDAD_AIRE_ENDPOINT)
    if data:
        save_json(data, "calidad_aire_madrid.json")
    return data

if __name__ == "__main__":
    scrape_calidad_aire_madrid()
