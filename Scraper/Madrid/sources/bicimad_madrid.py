from utils.fetch import fetch_json
from utils.save import save_json
from config import BICIMAD_ENDPOINT

def scrape_bicimad_madrid():
    data = fetch_json(BICIMAD_ENDPOINT)
    if data:
        save_json(data, "bicimad_madrid.json")
    return data

if __name__ == "__main__":
    scrape_bicimad_madrid()
