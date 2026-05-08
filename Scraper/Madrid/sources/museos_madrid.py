from utils.fetch import fetch_json
from utils.save import save_json
from config import MUSEOS_ENDPOINT

def scrape_museos_madrid():
    data = fetch_json(MUSEOS_ENDPOINT)
    if data:
        save_json(data, "museos_madrid.json")
    return data

if __name__ == "__main__":
    scrape_museos_madrid()
