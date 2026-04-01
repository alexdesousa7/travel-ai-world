# Este modulo contiene funciones para descargar HTML y JSON desde la web, con mensajes de errores y tiempo de espera.

import requests
from config import HEADERS

# Descarga de HTML en Wikipedia

def fetch_html(url):
    """Descarga el HTML de una pagina web y devuelve el contenido como texto"""

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo descargar el HTML de {url}")
        print(f"detalle: {e}")
        return None
    

# Descarga de JSON Datos de Madrid

def fetch_json(url):
    """Descarga un JSON desde una URL y devuelve un diccionario de Python"""
    try:
        response = request.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Error] No se pudo descargar el JSON desde {url}")
        print(f"Detalle: {e}")
        return None