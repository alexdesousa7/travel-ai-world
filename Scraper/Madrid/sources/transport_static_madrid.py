import json
from utils.save import save_json

def load_static_json(filename):
    try:
        with open(f"data/static/{filename}", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando archivo estático: {filename}")
        print(f"Detalle: {e}")
        return None


def scrape_transport_static():
    print("Cargando transporte estático...")

    metro = load_static_json("metro_madrid.json")
    if metro:
        save_json(metro, "metro_madrid.json")
        print("Metro estático OK")

    cercanias = load_static_json("cercanias_madrid.json")
    if cercanias:
        save_json(cercanias, "cercanias_madrid.json")
        print("Cercanías estático OK")

    emt = load_static_json("emt_paradas.json")
    if emt:
        save_json(emt, "emt_paradas.json")
        print("EMT estático OK")

    return {
        "metro": metro,
        "cercanias": cercanias,
        "emt": emt
    }
