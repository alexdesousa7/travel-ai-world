# 🏙️ Scraper de Madrid — Travel AI World

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data-blue?style=for-the-badge)


Este módulo implementa el **pipeline de ingesta de datos de la ciudad de Madrid**, utilizado por *Travel AI World* para recopilar información estructurada desde fuentes públicas y estables.  
Los datos generados se emplearán posteriormente para crear **embeddings** y alimentar la base vectorial del proyecto, permitiendo que la IA responda sobre Madrid con información propia.

---

## ✨ Fuentes de datos utilizadas

Actualmente, el scraper obtiene información desde:

### **📘 Wikipedia**
- Información general sobre Madrid  
- Lugares destacados  
- Contexto histórico y cultural  

### **🏛️ Datos Abiertos del Ayuntamiento de Madrid**
- Museos oficiales  
- Parques y zonas verdes  

Estas dos fuentes son **estables y funcionales**, y se integran automáticamente.

---

## 🚇 Transporte de Madrid (Metro, Cercanías, EMT)

### ❗ Importante

Tras múltiples pruebas se determinó que **no existen fuentes públicas estables** para obtener automáticamente:

- Estaciones de Metro  
- Estaciones de Cercanías  
- Paradas de EMT  

Las alternativas probadas (Overpass/OSM, OSMnx, Geoportal, repos comunitarios, MITMA, EMT API) resultaron:

- inestables,  
- incompletas,  
- con URLs rotas,  
- o dependientes de claves/API externas.

### ✔ Solución adoptada

Para mantener el scraper **estable y funcional**, se utiliza un **dataset estático mínimo**, ubicado en:

```
scraper/madrid/data/static/
```

Incluye:

- 5 estaciones representativas de Metro  
- 3 estaciones representativas de Cercanías  
- 3 paradas principales de EMT  

Estos datos permiten:

- evitar errores de scraping,  
- mantener el pipeline estable,  
- avanzar hacia la fase de IA,  
- y dejar abierta la puerta a ampliaciones futuras.

Más adelante se podrán sustituir por:

- datasets completos,  
- exportaciones manuales de OSM,  
- o la API oficial de EMT (requiere API KEY).

---

## 📂 Estructura del módulo

```
madrid/
│
├── main.py                 # Punto de entrada del scraper
│
├── sources/                # Scrapers por fuente
│   ├── wikipedia_madrid.py
│   ├── madrid_open_data.py
│   ├── geoportal_madrid.py
│   └── transport_static_madrid.py
│
├── utils/                  # Utilidades compartidas
│   ├── fetch.py
│   ├── parse.py
│   └── save.py
│
├── data/                   # Datos generados
│   ├── wikipedia_madrid.json
│   ├── museos_madrid.json
│   ├── parques_madrid.json
│   ├── metro_madrid.json
│   ├── cercanias_madrid.json
│   ├── emt_paradas.json
│   └── static/             # Datos estáticos de transporte
│       ├── metro_madrid.json
│       ├── cercanias_madrid.json
│       └── emt_paradas.json
│
└── README.md
```

---

## 🚀 Cómo ejecutar el scraper

Desde la carpeta del scraper:

```bash
cd scraper/madrid
python main.py
```

Esto ejecutará **todas las fuentes disponibles** y generará los archivos JSON dentro de:

```
scraper/madrid/data/
```

---

## 🧪 Ejecución por partes

Puedes ejecutar scrapers individuales desde Python:

```python
from sources.wikipedia_madrid import scrape_wikipedia_madrid
scrape_wikipedia_madrid()
```

O desde terminal:

```bash
python -c "from sources.madrid_open_data import scrape_madrid_open_data; scrape_madrid_open_data()"
```

---

## 🧹 Datos generados

Los archivos generados actualmente son:

- `wikipedia_madrid.json`  
- `museos_madrid.json`  
- `parques_madrid.json`  
- `metro_madrid.json`  
- `cercanias_madrid.json`  
- `emt_paradas.json`  

---

## 🛠️ Dependencias

Instala todas las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
requests
beautifulsoup4
lxml
```

No se requieren librerías GIS, APIs externas ni dependencias pesadas.

---

## 📌 Estado actual del scraper

✔️ Wikipedia  
✔️ Museos oficiales  
✔️ Parques y zonas verdes  
✔️ Transporte estático mínimo (Metro, Cercanías, EMT)  
✔️ Pipeline estable y sin errores  

Próximas integraciones previstas:

⬜ Eventos culturales  
⬜ Bicimad  
⬜ Calidad del aire  
⬜ Rutas recomendadas  
⬜ Transporte completo (cuando existan fuentes estables)

---

## 🎯 Objetivo del scraper

El propósito de este módulo es proporcionar **datos limpios, estructurados y estables** sobre Madrid para alimentar la IA del proyecto.  
El diseño modular permite añadir nuevas fuentes sin afectar al resto del sistema.


