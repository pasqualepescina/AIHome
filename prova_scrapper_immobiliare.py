from bs4 import BeautifulSoup
import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_url_immobiliare(url):
    try:
        logging.debug(f"Sending HTTP GET request to {url}")
        response = requests.get(url)

        if response.status_code == 200:
            logging.debug("Parsing the content using BeautifulSoup")
            soup = BeautifulSoup(response.content, 'html.parser')
            property_listings = str(soup.findAll())
            class_names = ['in-card__title', 'nd-figure__content', 'in-realEstateListCard__priceOnTop', 'in-realEstateListCard__features']
            elements = soup.find_all(class_=class_names)

            # Create a list to store the scraped data
            data = []

            # Create a dictionary to store the data for the current row
            row_data = {}

            # Extract the text content of each element found
            for element in elements:
                class_name = element['class'][0]  # Get the first class name of the element
                row_data[class_name] = element.get_text()
                if len(row_data) == len(class_names):
                    data.append(row_data.copy())
                    row_data.clear()
           # save_to_txt('Immobiliare/immobiliare_master.html', property_listings)

            return data

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        return None

def save_to_txt(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(data) + "\n")

        logging.info(f"Scraped data saved to {file_path}")

    except Exception as e:
        logging.error(f"Error while saving to {file_path}: {str(e)}")

base_url = 'https://www.immobiliare.it/vendita-case/milano/?pag='
max_pages = 1000  # Adjust this based on the number of pages you want to scrape

# Create a list to store all the scraped data
all_data = []

for page in range(1, max_pages + 1):
    url_to_scrape = f'{base_url}{page}'
    casait_info = scrape_url_immobiliare(url_to_scrape)

    if casait_info is not None:
        all_data.extend(casait_info)

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv('Immobiliare/immobiliare_clean.csv', index=False)

    print(df)
else:
    logging.warning("Failed to scrape or no data found.")
