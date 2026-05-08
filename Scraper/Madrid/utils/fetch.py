# Funciones para descargar HTML y JSON desde la web, con manejo de errores.

import requests
from config import HEADERS

# 
# DESCARGA DE HTML
# 

def fetch_html(url):
    """Descarga el HTML de una página web y devuelve el contenido como texto."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo descargar el HTML de {url}")
        print(f"Detalle: {e}")
        return None


# 
# DESCARGA DE JSON (Datos Abiertos Madrid)
# 

def fetch_json(url):
    """Descarga un JSON desde una URL y devuelve un diccionario de Python."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo descargar el JSON desde {url}")
        print(f"Detalle: {e}")
        return None
