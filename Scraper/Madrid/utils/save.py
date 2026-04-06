# Garantiza que todos los scrapers guardan datos con el mismo formato, evita errores de escritura, crea la carpeta data/ en caso de que no exista.

import json
import os
from config import DATA_DIR

# Guardar informacion en JSON

def save_json(data, filename):
    """Guarda un diccionario o lista en un archivo .JSON demtro de la carpeta data/"""
    # Crea la carpeta data/ en caso de que no exista
    os.makedirs(DATA_DIR, exist_ok=True)

    # Ruta completa del archivo
    filepath = os.path.join(DATA_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[OK] Archivo guardado: {filepath}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo {filepath}")
        print(f"Detalle: {e}")
