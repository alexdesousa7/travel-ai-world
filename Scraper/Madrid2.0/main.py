from sources.hoteles_madrid import get_hoteles_madrid
from sources.restaurantes_madrid import get_restaurantes_madrid
from sources.bares_madrid import get_bares_madrid
from sources.museos_madrid import get_museos_madrid
from sources.parques_madrid import get_parques_madrid
from sources.monumentos_madrid import get_monumentos_madrid

from sources.metro_madrid_wiki import get_metro_wiki
from sources.metro_fusion import fusionar_metro
from sources.metro_madrid import get_metro_madrid

from sources.cercanias_madrid_wiki import get_cercanias_wiki
from sources.cercanias_madrid_google import get_cercanias_google
from sources.cercanias_madrid_fusion import fusionar_cercanias

from sources.emt_madrid_wiki import get_emt_wiki
from sources.emt_madrid_google import get_emt_google
from sources.emt_madrid_fusion import fusionar_emt

from sources.iglesias_palacios_madrid import get_iglesias_palacios_madrid
from sources.iglesias_palacios_wiki import generar_wiki_iglesias_palacios
from sources.iglesias_palacios_fusion import fusionar_iglesias_palacios

from sources.historia_madrid import get_historia_madrid
from sources.cultura_madrid import get_cultura_madrid
from sources.gastronomia_madrid import get_gastronomia_madrid
from sources.clima_madrid import get_clima_madrid


import traceback


# ============================================================
# ORQUESTADOR PROFESIONAL
# ============================================================

def run_safe(nombre, funcion):
    print("\n----------------------------------------")
    print(f"   Ejecutando: {nombre}")
    print("----------------------------------------")

    try:
        funcion()
        print(f">> {nombre}: OK")
    except Exception as e:
        print(f">> ERROR en {nombre}: {e}")
        traceback.print_exc()
        print(">> Continuando con el siguiente módulo…")


# ============================================================
# MAIN
# ============================================================

def main():
    print("========================================")
    print("   Travel AI World - Madrid 2.0")
    print("========================================\n")

    # -------------------------
    # POIs (Google Places)
    # -------------------------
    run_safe("Hoteles", get_hoteles_madrid)
    run_safe("Restaurantes", get_restaurantes_madrid)
    run_safe("Bares", get_bares_madrid)
    run_safe("Museos", get_museos_madrid)
    run_safe("Parques", get_parques_madrid)
    run_safe("Monumentos", get_monumentos_madrid)

    # -------------------------
    # METRO
    # -------------------------
    run_safe("Metro - Wikipedia", get_metro_wiki)
    run_safe("Metro - Google Places", get_metro_madrid)
    run_safe("Metro - Fusionar", fusionar_metro)

    # -------------------------
    # CERCANÍAS
    # -------------------------
    run_safe("Cercanías - Wikipedia", get_cercanias_wiki)
    run_safe("Cercanías - Google Places", get_cercanias_google)
    run_safe("Cercanías - Fusionar", fusionar_cercanias)

    # -------------------------
    # EMT
    # -------------------------
    run_safe("EMT - Wikipedia", get_emt_wiki)
    run_safe("EMT - Google Places", get_emt_google)
    run_safe("EMT - Fusionar", fusionar_emt)

    # -------------------------
    # IGLESIAS Y PALACIOS
    # -------------------------
    run_safe("Iglesias/Palacios - Google Places", get_iglesias_palacios_madrid)
    run_safe("Iglesias/Palacios - Wikipedia", generar_wiki_iglesias_palacios)
    run_safe("Iglesias/Palacios - Fusionar", fusionar_iglesias_palacios)

    # -------------------------
    # DOCUMENTALES (Wikipedia)
    # -------------------------
    print("\n========================================")
    print("   MÓDULO DOCUMENTALES - MADRID")
    print("========================================")

    run_safe("Historia de Madrid", get_historia_madrid)
    run_safe("Cultura de Madrid", get_cultura_madrid)
    run_safe("Gastronomía de Madrid", get_gastronomia_madrid)
    run_safe("Clima de Madrid", get_clima_madrid)


    print("\n========================================")
    print("   PIPELINE COMPLETO FINALIZADO")
    print("========================================")


if __name__ == "__main__":
    main()
