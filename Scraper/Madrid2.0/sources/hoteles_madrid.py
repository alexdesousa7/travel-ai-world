import os
import json
import requests

from config.env import GOOGLE_API_KEY
from core.utils import normalize_hotel

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


def get_hoteles_madrid():
    print(">> Buscando hoteles en Madrid con Google Places (New)…")

    # 8 zonas estratégicas para cubrir la ciudad y tener variedad de hoteles para la AI a la hora de generar recomendaciones:
    zonas = [
        {"lat": 40.4168, "lng": -3.7038},  # Sol / Centro
        {"lat": 40.4653, "lng": -3.6883},  # Chamartín
        {"lat": 40.4218, "lng": -3.6821},  # Retiro / Salamanca
        {"lat": 40.4066, "lng": -3.6950},  # Atocha / Lavapiés
        {"lat": 40.4300, "lng": -3.7183},  # Moncloa / Argüelles
        {"lat": 40.4480, "lng": -3.7035},  # Tetuán / Cuatro Caminos
        {"lat": 40.4722, "lng": -3.5800},  # Barajas / Aeropuerto
        {"lat": 40.3925, "lng": -3.6620},  # Vallecas
    ]

    busquedas_texto = [
        "hotels in Madrid",
        "lodging Madrid",
        "accommodation Madrid",
        "hotel Madrid centro"
    ]

    hoteles = []
    ids_vistos = set()

    # ============================
    # 1) Nearby Search
    # ============================
    for idx, zona in enumerate(zonas, start=1):
        print(f">> Zona {idx}: {zona['lat']}, {zona['lng']}")

        payload = {
            "includedTypes": ["lodging"],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": zona["lat"],
                        "longitude": zona["lng"]
                    },
                    "radius": 7000
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_API_KEY,
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.location,places.rating,places.userRatingCount,places.types"
            )
        }

        response = requests.post(NEARBY_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        encontrados = data.get("places", [])
        print(f"   >> Hoteles encontrados en zona {idx}: {len(encontrados)}")

        for place in encontrados:
            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)
            hoteles.append(normalize_hotel(place))

    # ============================
    # 2) Text Search
    # ============================
    for query in busquedas_texto:
        print(f">> Búsqueda textual: '{query}'")

        payload = {
            "textQuery": query,
            "pageSize": 20
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_API_KEY,
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.location,places.rating,places.userRatingCount,places.types"
            )
        }

        response = requests.post(TEXT_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        encontrados = data.get("places", [])
        print(f"   >> Hoteles encontrados por texto: {len(encontrados)}")

        for place in encontrados:
            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)
            hoteles.append(normalize_hotel(place))

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "hotel",
        "count": len(hoteles),
        "items": hoteles,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/hoteles_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Hoteles guardados: {len(hoteles)}")
    return hoteles
