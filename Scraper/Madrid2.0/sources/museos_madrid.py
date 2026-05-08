import os
import json
import requests

from config.env import GOOGLE_API_KEY
from core.utils import normalize_museo

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


# ============================
# TIPOS VÁLIDOS (Museos + Galerías)
# ============================
TIPOS_VALIDOS = [
    "museum",
    "art_gallery"
]


# ============================
# TIPOS PROHIBIDOS
# ============================
TIPOS_PROHIBIDOS = [
    "church",
    "cathedral",
    "stadium",
    "shopping_mall",
    "park",
    "university",
    "library",
    "tourist_attraction",   # demasiado genérico si viene solo
    "lodging",
    "hotel"
]


# ============================
# MAPA TIPOS → TIPO DE MUSEO
# ============================
MAPA_TIPOS_MUSEO = {
    "museum": "Museo",
    "art_gallery": "Galería de Arte"
}


def es_museo_valido(types):
    # Excluir tipos prohibidos
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    # Aceptar si tiene museum o art_gallery
    if any(t in types for t in TIPOS_VALIDOS):
        return True

    return False


def inferir_tipo_museo(types):
    tipos = [MAPA_TIPOS_MUSEO[t] for t in types if t in MAPA_TIPOS_MUSEO]
    return tipos if tipos else ["Museo"]


# ============================
# SCRAPER PRINCIPAL
# ============================
def get_museos_madrid():
    print(">> Buscando museos en Madrid con Google Places (New)…")

    zonas = [
        {"lat": 40.4168, "lng": -3.7038},  # Sol / Centro
        {"lat": 40.4138, "lng": -3.6921},  # Museo del Prado / Retiro
        {"lat": 40.4251, "lng": -3.6883},  # Salamanca
        {"lat": 40.4100, "lng": -3.6940},  # Lavapiés / Reina Sofía
        {"lat": 40.4270, "lng": -3.7100},  # Conde Duque
        {"lat": 40.4500, "lng": -3.6900},  # Chamartín
        {"lat": 40.4300, "lng": -3.6700},  # Castellana
        {"lat": 40.4050, "lng": -3.7000},  # Embajadores
    ]

    busquedas_texto = [
        "museums in Madrid",
        "art galleries Madrid",
        "museos Madrid",
        "galerías de arte Madrid"
    ]

    museos = []
    ids_vistos = set()

    # ============================
    # 1) Nearby Search
    # ============================
    for idx, zona in enumerate(zonas, start=1):
        print(f">> Zona {idx}: {zona['lat']}, {zona['lng']}")

        payload = {
            "includedTypes": ["museum", "art_gallery"],
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
        print(f"   >> Museos encontrados en zona {idx}: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_museo_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_museo = inferir_tipo_museo(types)
            museo = normalize_museo(r, tipos_museo)
            museos.append(museo)

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
        print(f"   >> Museos encontrados por texto: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_museo_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_museo = inferir_tipo_museo(types)
            museo = normalize_museo(r, tipos_museo)
            museos.append(museo)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "museum",
        "count": len(museos),
        "items": museos,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/museos_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Museos guardados: {len(museos)}")
    return museos
