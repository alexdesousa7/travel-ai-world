import os
import json
import requests
from config.env import GOOGLE_API_KEY
from core.utils import normalize_restaurante

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
TEXT_URL = "https://places.googleapis.com/v1/places:searchText"


# ============================
# TIPOS DE COMIDA (lista blanca) - Si un lugar tiene alguno de estos tipos, lo consideramos restaurante
# ============================
TIPOS_VALIDOS = [
    "restaurant",
    "italian_restaurant",
    "japanese_restaurant",
    "mexican_restaurant",
    "chinese_restaurant",
    "burger_restaurant",
    "pizza_restaurant",
    "seafood_restaurant",
    "steak_house",
    "tapas_bar",
    "barbecue_restaurant",
    "vegan_restaurant",
    "vegetarian_restaurant",
    "thai_restaurant",
    "indian_restaurant",
    "korean_restaurant",
    "mediterranean_restaurant",
    "middle_eastern_restaurant",
    "spanish_restaurant",
    "latin_american_restaurant",
    "breakfast_restaurant",
    "coffee_shop",
    "cafe"
]


# ============================
# TIPOS PROHIBIDOS (lista negra) - Si un lugar tiene alguno de estos tipos, lo descartamos
# ============================
TIPOS_PROHIBIDOS = [
    "shopping_mall",
    "stadium",
    "arena",
    "supermarket",
    "grocery_store",
    "hotel",
    "lodging",
    "night_club",
    "event_venue",
    "sports_complex"
]



# ============================
# MAPA DE TIPOS → TIPO DE COMIDA
# ============================
MAPA_TIPOS_COMIDA = {
    "italian_restaurant": "Italiana",
    "japanese_restaurant": "Japonesa",
    "mexican_restaurant": "Mexicana",
    "chinese_restaurant": "China",
    "burger_restaurant": "Hamburguesas",
    "pizza_restaurant": "Pizza",
    "seafood_restaurant": "Mariscos",
    "steak_house": "Carnes",
    "tapas_bar": "Tapas",
    "barbecue_restaurant": "Barbacoa",
    "vegan_restaurant": "Vegana",
    "vegetarian_restaurant": "Vegetariana",
    "thai_restaurant": "Tailandesa",
    "indian_restaurant": "India",
    "korean_restaurant": "Coreana",
    "mediterranean_restaurant": "Mediterránea",
    "middle_eastern_restaurant": "Oriente Medio",
    "spanish_restaurant": "Española",
    "latin_american_restaurant": "Latinoamericana",
    "breakfast_restaurant": "Desayunos",
    "coffee_shop": "Cafetería",
    "cafe": "Café"
}


# ============================
# FUNCIONES DE FILTRO
# ============================
def es_restaurante_valido(types):
    # Si tiene un tipo prohibido → descartar
    if any(t in types for t in TIPOS_PROHIBIDOS):
        return False

    # Si tiene un tipo válido → aceptar
    if any(t in types for t in TIPOS_VALIDOS):
        return True

    # Si solo tiene "restaurant" → aceptar
    if "restaurant" in types:
        return True

    return False


def inferir_tipo_comida(types):
    tipos = [MAPA_TIPOS_COMIDA[t] for t in types if t in MAPA_TIPOS_COMIDA]
    return tipos if tipos else ["Variada"]


# ============================
# SCRAPER PRINCIPAL
# ============================
def get_restaurantes_madrid():
    print(">> Buscando restaurantes en Madrid con Google Places (New)…")

    # 8 zonas estratégicas para cubir la ciudad y tener variedad de restaurantes para la AI a la hora de generar recomendaciones:
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
        "restaurants in Madrid",
        "best restaurants Madrid",
        "food Madrid",
        "comida Madrid centro"
    ]

    restaurantes = []
    ids_vistos = set()

    # ============================
    # 1) Nearby Search
    # ============================
    for idx, zona in enumerate(zonas, start=1):
        print(f">> Zona {idx}: {zona['lat']}, {zona['lng']}")

        payload = {
            "includedTypes": ["restaurant"],
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
        print(f"   >> Restaurantes encontrados en zona {idx}: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_restaurante_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_comida = inferir_tipo_comida(types)
            restaurante = normalize_restaurante(r, tipos_comida)
            restaurantes.append(restaurante)

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
        print(f"   >> Restaurantes encontrados por texto: {len(encontrados)}")

        for r in encontrados:
            types = r.get("types", [])

            if not es_restaurante_valido(types):
                continue

            place_id = r.get("id")
            if place_id in ids_vistos:
                continue

            ids_vistos.add(place_id)

            tipos_comida = inferir_tipo_comida(types)
            restaurante = normalize_restaurante(r, tipos_comida)
            restaurantes.append(restaurante)

    # ============================
    # Guardar resultado final
    # ============================
    output = {
        "city": "Madrid",
        "category": "restaurant",
        "count": len(restaurantes),
        "items": restaurantes,
        "source": "Google Places API (New)"
    }

    os.makedirs("data", exist_ok=True)

    with open("data/restaurantes_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f">> Restaurantes guardados: {len(restaurantes)}")
    return restaurantes
