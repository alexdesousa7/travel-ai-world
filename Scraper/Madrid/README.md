# 🏙️ Scraper de Madrid — Travel AI World

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data-blue?style=for-the-badge)

Este módulo contiene el **pipeline de ingesta de datos de la ciudad de Madrid**, utilizado por *Travel AI World* para recopilar información estructurada desde múltiples fuentes oficiales.

Los datos generados se utilizan posteriormente para crear **embeddings** y alimentar la base vectorial del proyecto.

---

## ✨ Fuentes de datos utilizadas

El scraper de Madrid extrae información desde:

- **Wikipedia**  
  Lugares turísticos, monumentos, parques, museos destacados.

- **Datos Abiertos del Ayuntamiento de Madrid**  
  Museos oficiales, parques y jardines, eventos culturales, Bicimad, calidad del aire.

- **Geoportal Madrid**  
  Capas geográficas y datos espaciales relevantes.

---

## 📂 Estructura del módulo

```
madrid/
│
├── config.py               # URLs y endpoints de las fuentes
├── main.py                 # Punto de entrada del scraper
│
├── sources/                # Scrapers por fuente
│   ├── wikipedia_madrid.py
│   ├── madrid_open_data.py
│   └── geoportal_madrid.py
│
├── utils/                  # Utilidades compartidas
│   ├── fetch.py            # Descarga de HTML/JSON
│   ├── parse.py            # Limpieza y parsing
│   └── save.py             # Guardado en JSON
│
├── data/                   # Datos generados (ignorado por Git)
└── README.md
```

---

## 🚀 Cómo ejecutar el scraper

Desde la raíz del proyecto:

```bash
cd scraper/madrid
python main.py
```

Esto ejecutará todos los scrapers definidos y generará los JSON dentro de:

```
scraper/madrid/data/
```

---

## 🧪 Ejecución por partes

Puedes ejecutar scrapers individuales desde un intérprete Python:

```python
from sources.wikipedia_madrid import scrape_wikipedia_madrid
scrape_wikipedia_madrid()
```

O desde terminal:

```bash
python -c "from sources.wikipedia_madrid import scrape_wikipedia_madrid; scrape_wikipedia_madrid()"
```

---

## 🧹 Datos generados

Todos los archivos JSON se guardan en:

```
scraper/madrid/data/
```

Ejemplos:

- `lugares_turisticos.json`
- `monumentos.json`
- `parques.json`
- `museos_destacados.json`
- `museos_oficiales.json`
- `bicimad.json`
- `eventos.json`

> Estos archivos **no se suben al repositorio** gracias al `.gitignore`.

---

## 🛠️ Dependencias

Instala las dependencias necesarias:

```bash
pip install requests beautifulsoup4 lxml
```

Opcionalmente, puedes crear un `requirements.txt`:

```
requests
beautifulsoup4
lxml
```

---

## 🧩 Cómo extender el scraper

Para añadir nuevas fuentes:

1. Crear un archivo dentro de `sources/`  
2. Añadir la URL o endpoint en `config.py`  
3. Implementar la función de scraping  
4. Guardar los datos con `save_json()`  
5. Añadir la llamada en `main.py`

---

## 🎯 Objetivo del scraper

El propósito de este módulo es proporcionar **datos limpios, normalizados y actualizados** sobre Madrid para alimentar la IA del proyecto.  
Es un componente independiente del backend y del frontend, siguiendo buenas prácticas de arquitectura.

---