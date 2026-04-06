
# CONFIGURACIÓN GENERAL

# Carpeta donde se guardarán los JSON generados de Madrid

DATA_DIR = "data/"

# Headers para requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


# WIKIPEDIA


WIKIPEDIA_MADRID_URL = "https://es.wikipedia.org/wiki/Madrid"

# DATOS ABIERTOS MADRID (API)

# Base URL del portal de datos abiertos
MADRID_OPEN_DATA_BASE = "https://datos.madrid.es/egob/catalogo/"

# Endpoints útiles
MUSEOS_ENDPOINT = MADRID_OPEN_DATA_BASE + "201132-0-museos.json"
PARQUES_ENDPOINT = MADRID_OPEN_DATA_BASE + "202625-0-parques-jardines.json"
EVENTOS_ENDPOINT = MADRID_OPEN_DATA_BASE + "206974-0-agenda-eventos-culturales.json"
BICIMAD_ENDPOINT = MADRID_OPEN_DATA_BASE + "216619-0-bicimad-estaciones.json"
CALIDAD_AIRE_ENDPOINT = MADRID_OPEN_DATA_BASE + "210227-0-calidad-aire-estaciones.json"

# GEOPORTAL MADRID

GEO_MADRID_BASE = "https://geoportal.madrid.es/egob/catalogo/"

# Ejemplo de endpoint (lo afinaremos cuando lleguemos a este scraper)
GEO_COORDENADAS_ENDPOINT = GEO_MADRID_BASE + "coordenadas.json"

# HEADERS PARA REQUESTS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/html"
}
