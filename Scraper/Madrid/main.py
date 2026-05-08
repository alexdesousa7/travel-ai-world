
# main.py

from sources.restaurantes_madrid import scrape_restaurantes_madrid
from sources.hoteles_madrid import scrape_hoteles_madrid
from sources.hostales_madrid import scrape_hostales_madrid
from sources.monumentos_madrid import scrape_monumentos_madrid
from sources.fuentes_madrid import scrape_fuentes_madrid
from sources.hospitales_madrid import scrape_hospitales_madrid
from sources.barrios_madrid import scrape_barrios_madrid
from sources.info_general_madrid import scrape_info_general_madrid
from sources.rutas_turisticas_madrid import scrape_rutas_madrid
from sources.aeropuerto_madrid import scrape_aeropuerto_madrid
from sources.teatros_madrid import scrape_teatros_madrid
from sources.estadios_madrid import scrape_estadios_madrid
from sources.centros_comerciales_madrid import scrape_centros_comerciales_madrid
from sources.bares_madrid import scrape_bares_madrid
from sources.centros_informacion_madrid import scrape_centros_informacion_madrid
from sources.city_card_madrid import scrape_city_card_madrid




# Scrapers antiguos (APIs y datos abiertos)
from sources.museos_madrid import scrape_museos_madrid
from sources.parques_madrid import scrape_parques_madrid
from sources.eventos_madrid import scrape_eventos_madrid
from sources.bicimad_madrid import scrape_bicimad_madrid
from sources.calidad_aire_madrid import scrape_calidad_aire_madrid

def main():
    print("========================================")
    print("   Travel AI World - Scraper de Madrid  ")
    print("========================================\n")

    print(">> Scraping Restaurantes…")
    scrape_restaurantes_madrid()

    print(">> Scraping Hoteles…")
    scrape_hoteles_madrid()

    print(">> Scraping Hostales…")
    scrape_hostales_madrid()

    print(">> Scraping Monumentos…")
    scrape_monumentos_madrid()

    print(">> Scraping Fuentes…")
    scrape_fuentes_madrid()

    print(">> Scraping Hospitales…")
    scrape_hospitales_madrid()

    print(">> Scraping Barrios…")
    scrape_barrios_madrid()

    print(">> Scraping Información General…")
    scrape_info_general_madrid()

    print(">> Scraping Rutas Turísticas…")
    scrape_rutas_madrid()

    print(">> Scraping Aeropuerto Barajas…")
    scrape_aeropuerto_madrid()

    print("\n>> Scraping Museos (Datos Abiertos)…")
    scrape_museos_madrid()

    print(">> Scraping Parques (Datos Abiertos)…")
    scrape_parques_madrid()

    print(">> Scraping Eventos (Datos Abiertos)…")
    scrape_eventos_madrid()

    print(">> Scraping BiciMAD (Datos Abiertos)…")
    scrape_bicimad_madrid()

    print(">> Scraping Calidad del Aire (Datos Abiertos)…")
    scrape_calidad_aire_madrid()

    print(">> Scraping Teatros…")
    scrape_teatros_madrid()

    print(">> Scraping Estadios…")
    scrape_estadios_madrid()

    print(">> Scraping Centros Comerciales…")
    scrape_centros_comerciales_madrid()

    print(">> Scraping Bares…")
    scrape_bares_madrid()

    print(">> Scraping Centros de Información Turística…")
    scrape_centros_informacion_madrid()

    print(">> Scraping Madrid City Card…")
    scrape_city_card_madrid()




    print("\n==========================================")
    print("   Scraping Madrid completado correctamente ")
    print("============================================")

if __name__ == "__main__":
    main()
