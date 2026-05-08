# 🏙️ Scraper de Madrid — Versión Antigua (Madrid Old)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data-blue?style=for-the-badge)


Este módulo corresponde a la **primera versión del scraper de Madrid**, utilizado en las fases iniciales del proyecto *Travel AI World*.  
Se mantiene en el repositorio **solo como referencia histórica y documental**, ya que su arquitectura y fuentes de datos fueron reemplazadas por la nueva versión **Madrid 2.0**.

---

## ❌ Limitaciones de Madrid Old

Tras varios meses de pruebas, se identificaron problemas estructurales que hacían imposible mantener este scraper en producción:

### 🔹 1. Dependencia de fuentes inestables
- URLs del Ayuntamiento que cambiaban sin aviso  
- Endpoints JSON que desaparecían  
- Geoportal con rutas rotas  
- Falta de consistencia en los datos  

### 🔹 2. Falta de cobertura real
Madrid Old solo podía obtener:

- Museos oficiales  
- Parques  
- Algunos eventos  
- Información parcial de Wikipedia  

No existía forma fiable de obtener:

- Restaurantes  
- Hoteles  
- Bares  
- Monumentos  
- Iglesias  
- Palacios  
- Transporte completo  

### 🔹 3. Arquitectura rígida y difícil de extender
- Módulos acoplados  
- Falta de normalización  
- Sin fusiones entre fuentes  
- Sin manejo de errores  
- Sin orquestador  

### 🔹 4. No apto para IA
Los datos generados eran:

- incompletos  
- inconsistentes  
- no normalizados  
- insuficientes para embeddings  

---

## ✔ Por qué nació Madrid 2.0

Madrid 2.0 se creó para resolver todos los problemas anteriores y ofrecer:

### 🟩 1. **Cobertura completa de la ciudad**
Gracias a Google Places API:

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

### 🟩 2. **Datos enriquecidos con Wikipedia**
- Historia  
- Arquitectura  
- Estilo  
- Año de construcción  
- Información documental  

### 🟩 3. **Arquitectura modular y profesional**
- `sources/` → scrapers atómicos  
- `core/` → utilidades  
- `main.py` → orquestador  
- `data/` → datasets finales  

### 🟩 4. **Pipeline estable y sin errores**
- Manejo de errores por módulo  
- Logs claros  
- Fusión entre fuentes  
- Normalización consistente  

---

## 📌 ¿Por qué se mantiene Madrid Old?

Aunque ya no se usa en producción, se conserva porque:

- contiene código útil como referencia  
- documenta la evolución del proyecto  
- sirve como base para futuros scrapers documentales  
- permite comparar la mejora entre versiones  

---

## 📈 Diferencias clave: Madrid Old vs Madrid 2.0

| Característica | Madrid Old | Madrid 2.0 |
|----------------|------------|-------------|
| Fuentes | Wikipedia + Open Data | Google Places + Wikipedia |
| Estabilidad | Baja | Alta |
| Cobertura | Parcial | Completa |
| Arquitectura | Rígida | Modular |
| Normalización | Inconsistente | Profesional |
| Uso para IA | Limitado | Óptimo |
| Transporte | Estático mínimo | Completo (Metro, EMT, Cercanías) |

---

## 🎯 Conclusión

Madrid Old fue un buen punto de partida, pero Madrid 2.0 es la versión que:

- **permite escalar**,  
- **es estable**,  
- **es completa**,  
- **y es apta para IA**.

Madrid Old se mantiene únicamente como **contenido documental y referencia histórica** del proyecto.

