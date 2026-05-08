# 🏙️ Madrid 2.0 — Scraper Oficial de Travel AI World

`https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python`
`https://img.shields.io/badge/Google%20Places-API-blue?style=for-the-badge`
`https://img.shields.io/badge/Wikipedia-Scraper-black?style=for-the-badge`
`https://img.shields.io/badge/JSON-Data-green?style=for-the-badge`

**Madrid 2.0** es la nueva versión del scraper oficial de *Travel AI World*, diseñado para generar datos limpios, completos y estructurados sobre la ciudad de Madrid.

Es la evolución directa del scraper antiguo de **Madrid**, resolviendo todas sus limitaciones y añadiendo:

- cobertura total de POIs,  
- transporte completo,  
- enriquecimiento documental,  
- arquitectura modular,  
- y un pipeline profesional y estable.

---

# 🚀 ¿Por qué Madrid 2.0?

El antiguo scraper de Madrid  dependía de fuentes inestables (Open Data, Geoportal) y no podía obtener:

- restaurantes  
- hoteles  
- bares  
- monumentos  
- iglesias  
- palacios  
- transporte público completo  

Madrid 2.0 utiliza:

---

## 🟩 Google Places API  
Para obtener POIs reales, actualizados y completos:

- Hoteles  
- Restaurantes  
- Bares  
- Museos  
- Monumentos  
- Parques  
- Iglesias y Palacios  
- Estaciones de Metro  
- Estaciones de Cercanías  
- Intercambiadores EMT  

---

## 🟩 Wikipedia  
Para enriquecer:

- historia  
- cultura  
- gastronomía  
- clima  
- arquitectura  
- estilo  
- año de construcción  

---

## 🟩 Arquitectura modular  
- `sources/` → scrapers atómicos  
- `core/` → utilidades  
- `main.py` → orquestador  
- `data/` → datasets generados  

---

## 🟦 Uso de Google Places API
Madrid 2.0 utiliza Google Places API (New) como fuente principal para obtener información actualizada y precisa sobre los puntos de interés de la ciudad.

Se emplean los siguientes endpoints oficiales:

- Nearby Search — para obtener POIs por coordenadas
- Text Search — para búsquedas semánticas
- Place Details — para enriquecer cada POI con datos adicionales

Gracias a estos endpoints, el scraper obtiene:

- nombre del lugar
- dirección
- coordenadas
- rating y número de reseñas
- tipos de establecimiento
- horarios
- teléfono
- website

Google Places garantiza:

- datos actualizados
- alta cobertura
- consistencia global
- fiabilidad para sistemas de IA

Este proyecto utiliza Google Places API conforme a sus Términos de Servicio.  
Los datos se emplean exclusivamente para alimentar el sistema Travel AI World.


# 📂 Estructura del proyecto

```
Madrid2.0/
│
├── main.py                 # Orquestador del pipeline completo
│
├── sources/                # Scrapers por categoría
│   ├── hoteles_madrid.py
│   ├── restaurantes_madrid.py
│   ├── bares_madrid.py
│   ├── museos_madrid.py
│   ├── monumentos_madrid.py
│   ├── parques_madrid.py
│   ├── iglesias_palacios_madrid.py
│   ├── iglesias_palacios_wiki.py
│   ├── iglesias_palacios_fusion.py
│   ├── metro_madrid.py
│   ├── metro_madrid_wiki.py
│   ├── metro_fusion.py
│   ├── cercanias_madrid_google.py
│   ├── cercanias_madrid_wiki.py
│   ├── cercanias_madrid_fusion.py
│   ├── emt_madrid_google.py
│   ├── emt_madrid_wiki.py
│   ├── emt_madrid_fusion.py
│
│   ├── historia_madrid.py          # Documentales
│   ├── cultura_madrid.py
│   ├── gastronomia_madrid.py
│   ├── clima_madrid.py
│
├── core/
│   ├── utils.py
│
├── data/                   # Datos generados
│   ├── hoteles_madrid.json
│   ├── restaurantes_madrid.json
│   ├── bares_madrid.json
│   ├── museos_madrid.json
│   ├── monumentos_madrid.json
│   ├── parques_madrid.json
│   ├── iglesias_palacios_final.json
│   ├── metro_madrid_final.json
│   ├── cercanias_madrid_final.json
│   ├── emt_madrid_final.json
│
│   ├── historia_madrid.json        # Documentales
│   ├── cultura_madrid.json
│   ├── gastronomia_madrid.json
│   ├── clima_madrid.json
│
└── README.md
```

---

# 🧠 ¿Qué aporta Madrid 2.0?

### ✔ Datos completos  
Cobertura total de POIs, transporte y contenido documental.

### ✔ Datos actualizados  
Google Places garantiza frescura y precisión.

### ✔ Datos normalizados  
Estructura uniforme en todos los JSON.

### ✔ Datos fusionados entre fuentes  
Wikipedia + Google Places → datasets enriquecidos.

### ✔ Datos aptos para embeddings  
Especialmente los módulos documentales.

### ✔ Pipeline estable y sin errores  
Orquestado con `run_safe()`.

### ✔ Preparado para IA generativa  
Datos limpios, consistentes y listos para vectorización.

---

# 📘 Módulo Documentales (Wikipedia)

Madrid 2.0 incluye un bloque especial de **contenido narrativo**, ideal para embeddings:

### 🟦 Historia  
13 secciones completas desde Wikipedia REST API.

### 🟦 Cultura  
Sección cultural del artículo principal de Madrid.

### 🟦 Gastronomía  
Platos, ingredientes, costumbres y tradición culinaria.

### 🟦 Clima  
Descripción climática estable (Köppen, temperaturas, precipitaciones).

Estos módulos permiten que la IA:

- explique Madrid,  
- genere contexto,  
- responda preguntas complejas,  
- y produzca contenido narrativo coherente.

---

# 🏁 Cómo ejecutar

```bash
python main.py
```

Esto ejecuta:

- todos los scrapers  
- todas las fusiones  
- todos los enriquecimientos  
- y genera todos los JSON finales  

---

# 📈 Diferencias clave con Madrid Old

| Característica    | Madrid Old            | Madrid 2.0                |
| ---               | ---                   | ---                       |
| Fuentes           | Wikipedia + Open Data | Google Places + Wikipedia |
| Estabilidad       | Baja                  | Alta                      |
| Cobertura         | Parcial               | Completa                  |
| Transporte        | Estático              | Completo (Metro, Renfe, EMT) |
| Normalización     | Inconsistente         | Profesional               |
| Documentales      | No                    | Sí (Historia, Cultura, Gastronomía, Clima) |
| Uso para IA       | Limitado              | Óptimo                    |

---

# 📌 Estado actual del proyecto

### ✔ POIs completos  
### ✔ Transporte completo  
### ✔ Iglesias y Palacios fusionados  
### ✔ Documentales completados  
### ✔ Pipeline estable  
### ✔ Datos listos para embeddings  

---

# 🛣️ Roadmap

### 🔜 Próximos pasos
- Integración de **Madrid Open Data** (barrios, distritos, población, geometrías).  
- Normalización avanzada de POIs.  
- Generación de embeddings automáticos.  
- Integración con el backend de Travel AI World.  
- Dashboard de validación de datos.  

---