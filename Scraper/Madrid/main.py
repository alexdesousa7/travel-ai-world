from sources.wikipedia_madrid import scrape_wikipedia_madrid
from sources.madrid_open_data import scrape_madrid_open_data
from sources.geoportal_madrid import scrape_geoportal_madrid
from sources.transport_static_madrid import scrape_transport_static



def run_all():
    print("Sraper solo Ciudad Madrid")

    scrape_wikipedia_madrid()
    scrape_madrid_open_data()
    scrape_geoportal_madrid()
    scrape_transport_static()


    print("Scraper Finalizado Ciudad Madrid")


if __name__ == "__main__":
    run_all()
