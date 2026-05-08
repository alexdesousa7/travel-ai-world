from utils.fetch import fetch_json
from utils.save import save_json
from config import PARQUES_ENDPOINT

def scrape_parques_madrid():
    data = fetch_json(PARQUES_ENDPOINT)
    if data:
        save_json(data, "parques_madrid.json")
    return data

if __name__ == "__main__":
    scrape_parques_madrid()
