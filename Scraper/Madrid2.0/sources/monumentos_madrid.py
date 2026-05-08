import os
import json
import requests

from config.env import GOOGLE_API_KEY
from core.utils import normalize_monumento

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


# ============================
# TIPOS VÁLIDOS
# ============================
TIPOS_VALIDOS = [
    "monument",
    "landmark",
    "historical_landmark",
    "tourist_attraction"
]


# ============================
# TIPOS PROHIBIDOS
# ============================
TIPOS_PROHIBIDOS = [
    "museum",
    "art_gallery",
    "park",
    "natural_feature",
    "square",
    "church",
    "cathedral",
    "stadium",
    "shopping_mall",
    "university",
    "library",
    "lodging",
    "hotel"
]


# ============================
# MAPA TIPOS → TIPO MONUMENTO
# ============================
MAPA_TIPOS_MONUMENTO = {
    "monument": "Monumento",
    "landmark": "Lugar Emblemático",
    "historical_landmark": "Lugar Histórico",
    "tourist_attraction": "Atracción Turística"
}


def es_monumento_valido(types):
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    if any(t in types for t in TIPOS_VALIDOS):
        return True

    return False


def inferir_tipo_monumento(types):
    tipos = [MAPA_TIPOS_MONUMENTO[t] for t in types if t in MAPA_TIPOS_MONUMENTO]
    return tipos if tipos else ["Monumento"]


def get_monumentos_madrid():
    print(">> Buscando monumentos en Madrid con Google Places (New)…")

    zonas = [
        {"lat": 40.4168, "lng": -3.7038},  # Centro
        {"lat": 40.4200, "lng": -3.7100},  # Palacio Real
        {"lat": 40.4150, "lng": -3.7070},  # Sol
        {"lat": 40.4250, "lng": -3.6900},  # Salamanca
        {"lat": 40.4100, "lng": -3.6950},  # Lavapiés
        {"lat": 40.4300, "lng": -3.7200},  # Moncloa
        {"lat": 40.4500, "lng": -3.6900},  # Chamartín
        {"lat": 40.4050, "lng": -3.7000},  # Embajadores
    ]

    busquedas_texto = [
        "monuments in Madrid",
        "historical landmarks Madrid",
        "statues Madrid",
        "monumentos Madrid",
        "lugares históricos Madrid"
    ]

    monumentos = []
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

            if not es_monumento_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_monumento = inferir_tipo_monumento(types)
            monumento = normalize_monumento(place, tipos_monumento)
            monumentos.append(monumento)

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
        print(f"   >> Monumentos encontrados por texto: {len(encontrados)}")

        for place in encontrados:
            types = place.get("types", [])

            if not es_monumento_valido(types):
                continue

            place_id = place.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_monumento = inferir_tipo_monumento(types)
            monumento = normalize_monumento(place, tipos_monumento)
            monumentos.append(monumento)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "monument",
        "count": len(monumentos),
        "items": monumentos,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/monumentos_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Monumentos guardados: {len(monumentos)}")
    return monumentos
