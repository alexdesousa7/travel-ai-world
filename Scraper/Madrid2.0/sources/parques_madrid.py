import os
import json
import requests

from config.env import GOOGLE_API_KEY
from core.utils import normalize_parque

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


TIPOS_VALIDOS = [
    "park",
    "natural_feature",
    "square"
]

TIPOS_PROHIBIDOS = [
    "museum",
    "art_gallery",
    "church",
    "cathedral",
    "stadium",
    "shopping_mall",
    "university",
    "library",
    "lodging",
    "hotel"
]


MAPA_TIPOS_PARQUE = {
    "park": "Parque",
    "natural_feature": "Espacio Natural",
    "square": "Plaza"
}


def es_parque_valido(types):
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    if any(t in types for t in TIPOS_VALIDOS):
        return True

    return False


def inferir_tipo_parque(types):
    tipos = [MAPA_TIPOS_PARQUE[t] for t in types if t in MAPA_TIPOS_PARQUE]
    return tipos if tipos else ["Parque"]


def get_parques_madrid():
    print(">> Buscando parques en Madrid con Google Places (New)…")

    zonas = [
        {"lat": 40.4168, "lng": -3.7038},
        {"lat": 40.4138, "lng": -3.6921},
        {"lat": 40.4251, "lng": -3.6883},
        {"lat": 40.4100, "lng": -3.6940},
        {"lat": 40.4270, "lng": -3.7100},
        {"lat": 40.4500, "lng": -3.6900},
        {"lat": 40.4300, "lng": -3.6700},
        {"lat": 40.4050, "lng": -3.7000},
    ]

    busquedas_texto = [
        "parks in Madrid",
        "gardens Madrid",
        "plazas Madrid",
        "parques Madrid",
        "jardines Madrid"
    ]

    parques = []
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

            if not es_parque_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_parque = inferir_tipo_parque(types)
            parque = normalize_parque(place, tipos_parque)
            parques.append(parque)

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
        print(f"   >> Parques encontrados por texto: {len(encontrados)}")

        for place in encontrados:
            types = place.get("types", [])

            if not es_parque_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_parque = inferir_tipo_parque(types)
            parque = normalize_parque(place, tipos_parque)
            parques.append(parque)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "park",
        "count": len(parques),
        "items": parques,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/parques_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Parques guardados: {len(parques)}")
    return parques
