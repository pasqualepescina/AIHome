import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_annuncio_items(url):
    try:
        # Send an HTTP GET request to the URL
        logging.debug(f"Sending HTTP GET request to {url}")
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the web page using BeautifulSoup
            logging.debug("Parsing the content using BeautifulSoup")
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the listings with class "annuncio-item" on the page
            annuncio_items = soup.find_all('li', class_='annuncio-item')

            # Return the list of scrapped data
            return annuncio_items

        else:
            logging.error(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        return None

def save_to_txt(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(str(item) + "\n")
                file.write("-" * 40 + "\n")

        logging.info(f"Scraped data saved to {file_path}")

    except Exception as e:
        logging.error(f"Error while saving to {file_path}: {str(e)}")

# URL to scrape
url_to_scrape = 'https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html'

# Scrape the data
scraped_annuncio_items = scrape_annuncio_items(url_to_scrape)

# Save the scraped data to a text file
if scraped_annuncio_items is not None:
    file_path = 'scraped_data.txt'
    save_to_txt(file_path, scraped_annuncio_items)
else:
    logging.warning("Failed to scrape or no data found.")