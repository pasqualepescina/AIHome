import logging
from scrape_master_url import scrape_url_master

def scrape_tecnocasa_url():
    try:
        tecnocasa_url = "https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html"
        logging.info(f"Starting to scrape {tecnocasa_url}")
        scraped_annuncio_items = scrape_url_master(tecnocasa_url)
    except Exception as e:
        logging.error(f"Error while scraping {tecnocasa_url}: {str(e)}")
