from bs4 import BeautifulSoup

# Parseo del HTML 

def parse_html_list(html, section_id):
    """Extrae una lista de una seccion de Wikipedia, section_id es el ID del encabezado de la seccion o las secciones"""
    soup = BeautifulSoup(html, "html.parser")

    # Buscar la seccion por su ID
    section = soup.find("span", {"id": section_id})
    if not section:
        print(f"[WARN] No se encontro una lista <ul> despues de {section_id}")
        return []
    
    # extraer los elementos de la lista
    items = [li.get_text(strip=True) for li in ul.find_all("li")]
    return items


# Limpieza y depuracion de texto y datos

def clean_text(text):
    """Limpieza de texto eliminando saltos de linea, espacios doble, etc"""
    if not isinstance(text, str):
        return text
    
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split()) # Deberia de eliminar espacios multiples
    return text

# Normalizacion de datos

def normalize_record(record):
    """Normaliza un diccionario, limpia todos los valores string y elimina claves vacias"""
    cleanrecord = {}

    for key, value in record.items():
        if isinstance(value, str):
            value = clean_text(value)

        if value not in [None, "", [], {}]:
            clean_record[key] = value
    
    return clean_record