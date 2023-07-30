import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_url_master_tecnocasa(url):
    try:
        # Send an HTTP GET request to the URL
        logging.debug(f"Sending HTTP GET request to {url}")
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the web page using BeautifulSoup
            logging.debug("Parsing the content using BeautifulSoup")
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the <template> tag with the slot="cities-seo-list" attribute
            template_tag = soup.find('template', attrs={'slot': 'cities-seo-list'})

            # If the <template> tag is found, find all the <span> tags with URLs under it
            if template_tag:
                logging.debug("Get Urls from further scrapping")
                cities_spans = template_tag.find_all('span')
                urls = [span.a['href'] for span in cities_spans if span.a]

                return urls

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

        logging.info(f"Scraped data saved to {file_path}")

    except Exception as e:
        logging.error(f"Error while saving to {file_path}: {str(e)}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_tecnocasa_data(url):
    """
    Scrape data from a single URL.

    Parameters:
        url (str): The URL to scrape.

    Returns:
        str: The extracted data from the URL (for demonstration, we return the title of the page).
             Modify this function to extract other relevant information based on your requirements.
    """
    try:
        # Send an HTTP GET request to the URL
        logging.debug(f"Sending HTTP GET request to {url}")
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the web page using BeautifulSoup
            logging.debug("Parsing the content using BeautifulSoup")
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title of the page (for demonstration purposes)
            title = soup.title.string.strip()
            return title

        else:
            logging.error(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        return None

def scrape_multiple_urls(urls_file):
    """
    Scrape data from multiple URLs listed in a file.

    Parameters:
        urls_file (str): Path to the file containing the URLs to scrape.

    Returns:
        list: A list of extracted data from each URL (for demonstration, we return the titles of the pages).
              Modify the scrape_tecnocasa_data function to extract other relevant information as needed.
    """
    try:
        with open(urls_file, 'r') as file:
            urls = file.read().splitlines()

        scraped_data = []
        for url in urls:
            data = scrape_tecnocasa_data(url)
            if data:
                scraped_data.append(data)

        return scraped_data

    except Exception as e:
        logging.error(f"Error while reading URLs from {urls_file}: {str(e)}")
        return None
# Print the scraped data
if scraped_data:
    logging.info("Scraped Data:")
    for data in scraped_data:
        logging.info(data)
else:
    logging.warning("Failed to scrape or no data found.")

# MASTER URL TO SCRAPE AND GET ALK THE OTHERS
url_to_scrape = 'https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html'

# Scrape the data
scraped_annuncio_items = scrape_url_master_tecnocasa(url_to_scrape)

# Save the scraped data to a text file
if scraped_annuncio_items is not None:
    file_path = 'urls_to_scrape_tecnocasa.txt'
    save_to_txt(file_path, scraped_annuncio_items)
else:
    logging.warning("Failed to scrape or no data found.")