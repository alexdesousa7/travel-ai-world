import os
import json
import requests

from config.env import GOOGLE_API_KEY
from core.utils import normalize_metro

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


# ============================
# TIPOS VÁLIDOS
# ============================
TIPOS_VALIDOS = [
    "subway_station",
    "transit_station"
]


# ============================
# TIPOS PROHIBIDOS
# ============================
TIPOS_PROHIBIDOS = [
    "bus_station",
    "light_rail_station",
    "airport",
    "parking",
    "taxi_stand",
    "tram_station"
]


def es_metro_valido(types):
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    if any(t in types for t in TIPOS_VALIDOS):
        return True

    return False


def get_metro_madrid():
    print(">> Buscando estaciones de Metro en Madrid con Google Places (New)…")

    zonas = [
        {"lat": 40.4168, "lng": -3.7038},  # Centro
        {"lat": 40.4200, "lng": -3.7100},  # Palacio Real
        {"lat": 40.4250, "lng": -3.6900},  # Salamanca
        {"lat": 40.4100, "lng": -3.6950},  # Lavapiés
        {"lat": 40.4300, "lng": -3.7200},  # Moncloa
        {"lat": 40.4500, "lng": -3.6900},  # Chamartín
        {"lat": 40.4050, "lng": -3.7000},  # Embajadores
        {"lat": 40.4700, "lng": -3.5800},  # Barajas
    ]

    busquedas_texto = [
        "metro station Madrid",
        "estación de metro Madrid",
        "subway Madrid",
        "metro Madrid"
    ]

    estaciones = []
    ids_vistos = set()

    # ============================
    # 1) Nearby Search (sin includedTypes)
    # ============================
    for idx, zona in enumerate(zonas, start=1):
        print(f">> Zona {idx}: {zona['lat']}, {zona['lng']}")

        payload = {
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
        print(f"   >> Resultados brutos: {len(encontrados)}")

        for place in encontrados:
            types = place.get("types", [])

            if not es_metro_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            estacion = normalize_metro(place, lineas=[])
            estaciones.append(estacion)

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
        print(f"   >> Estaciones encontradas por texto: {len(encontrados)}")

        for place in encontrados:
            types = place.get("types", [])

            if not es_metro_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            estacion = normalize_metro(place, lineas=[])
            estaciones.append(estacion)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "metro",
        "count": len(estaciones),
        "items": estaciones,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/metro_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Estaciones guardadas: {len(estaciones)}")
    return estaciones
