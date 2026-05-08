import os
import json
import requests
from config.env import GOOGLE_API_KEY
from core.utils import normalize_restaurante  # reutilizamos normalizador base

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


# ============================
# TIPOS VÁLIDOS PARA BARES (Opción B)
# ============================
TIPOS_VALIDOS = [
    "bar",
    "pub",
    "cocktail_bar",
    "wine_bar",
    "tapas_bar",
    "brewpub",
    "beer_bar",
    "lounge",
    "restaurant",  # algunos bares vienen marcados como restaurant
]


# ============================
# TIPOS PROHIBIDOS
# ============================
TIPOS_PROHIBIDOS = [
    "night_club",
    "shopping_mall",
    "stadium",
    "arena",
    "supermarket",
    "grocery_store",
    "hotel",
    "lodging",
    "event_venue",
    "sports_complex"
]


# ============================
# MAPA DE TIPOS → TIPO DE BAR
# ============================
MAPA_TIPOS_BAR = {
    "bar": "Bar",
    "pub": "Pub",
    "cocktail_bar": "Coctelería",
    "wine_bar": "Wine Bar",
    "tapas_bar": "Tapas",
    "brewpub": "Brewpub",
    "beer_bar": "Cervecería",
    "lounge": "Lounge",
}


# ============================
# FUNCIONES DE FILTRO
# ============================
def es_bar_valido(types):
    # Excluir tipos prohibidos
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    # Aceptar si tiene un tipo válido
    if any(t in types for t in TIPOS_VALIDOS):
        return True

    return False


def inferir_tipo_bar(types):
    tipos = [MAPA_TIPOS_BAR[t] for t in types if t in MAPA_TIPOS_BAR]
    return tipos if tipos else ["Bar"]


# ============================
# SCRAPER PRINCIPAL
# ============================
def get_bares_madrid():
    print(">> Buscando bares en Madrid con Google Places (New)…")

    # 8 zonas estratégicas para cubrir la ciudad y tener una variedad de bares para la AI
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

    # Búsquedas textuales
    busquedas_texto = [
        "bars in Madrid",
        "pubs in Madrid",
        "cocktail bars Madrid",
        "wine bars Madrid",
        "bares Madrid centro"
    ]

    bares = []
    ids_vistos = set()

    # ============================
    # 1) Nearby Search
    # ============================
    for idx, zona in enumerate(zonas, start=1):
        print(f">> Zona {idx}: {zona['lat']}, {zona['lng']}")

        payload = {
            "includedTypes": ["bar"],
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
        print(f"   >> Bares encontrados en zona {idx}: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_bar_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_bar = inferir_tipo_bar(types)
            bar = normalize_restaurante(r, tipos_bar)
            bares.append(bar)

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
        print(f"   >> Bares encontrados por texto: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_bar_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_bar = inferir_tipo_bar(types)
            bar = normalize_restaurante(r, tipos_bar)
            bares.append(bar)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "bar",
        "count": len(bares),
        "items": bares,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/bares_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Bares guardados: {len(bares)}")
    return bares
