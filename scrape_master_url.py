from bs4 import BeautifulSoup
import logging
import requests 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def scrape_url_master_tecnocasa(url):
    try:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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