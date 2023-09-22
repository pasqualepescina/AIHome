import requests
from bs4 import BeautifulSoup
import logging
import os
import json
import pandas as pd
from scrape_master_url import scrape_url_master

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a folder named "Tecnocasa" if it doesn't exist
# MASTER URL TO SCRAPE AND GET ALK THE OTHERS
urls_masters_to_scrappe = ["https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html", "https://www.immobiliare.it/vendita-case/milano/?pag="]

# Scrape the data
for url in urls_masters_to_scrappe:
    logging.info(f"Starting to scrape {url}")
    scraped_annuncio_items = scrape_url_master(url)


    

