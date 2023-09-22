import os
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
from scrape_html_childs import scrape_multiple_urls, scrape_html_files, scrape_url_immobiliare, save_to_txt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_url_master(url):
    try:
        logging.info(f"Sending HTTP GET request to {url}")
        response = requests.get(url)
        logging.info(response.status_code)
        if response.status_code == 200:
            print('got response 200')
            if 'tecnocasa' in url:
                logging.info('Correctly detected tecnocasa url')
                output_folder = "Tecnocasa"
                logging.info(f"Output folder set to {output_folder}")
                soup = BeautifulSoup(response.content, 'html.parser')
                logging.debug("Parsing the content of {url}")

                template_tag = soup.find('template', attrs={'slot': 'cities-seo-list'})
                        # Scrape data from the listed URLs and create files for each URL
      # Get a list of all the files in the directory
                if template_tag:
                    logging.debug("Get Urls from further scrapping")
                    cities_spans = template_tag.find_all('span')
                    urls = [span.a['href'] for span in cities_spans if span.a]
                    file_path = r'C:\Users\pesci\OneDrive\Desktop\AIHome\AIHome\Tecnocasa\urls_to_scrape_tecnocasa.txt'
                    save_to_txt(file_path, urls)
                    logging.info("Correctly created txt of childs urls")
                    results_scrapper =scrape_html_files(scrape_multiple_urls(file_path))
                    combined_data = {}
                        
                    for data in results_scrapper:
                        for key, value in data.items():
                            combined_data.setdefault(key, []).extend(value)
                    df = pd.DataFrame(combined_data)
                    #df.drop_duplicates(inplace=True)
                    #output_csv = os.path.join(, "tecnocasa.csv")
                    df.to_csv(r'C:\Users\pesci\OneDrive\Desktop\AIHome\AIHome\Tecnocasa\data_tecnocasa.csv', index=False)
                    logging.debug("Data saved to CSV")

            elif 'immobiliare' in url:
                all_data = []
                max_pages = 80
                output_folder = 'Immobiliare'

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                property_listings = str(soup.findAll())
                file_path = 'immobiliare.html'
                property_listings = str(soup.findAll())
                save_to_txt(file_path, property_listings)
                
                if os.path.getsize(file_path) > 0:
                    for page in range(1, max_pages + 1):
                        url_to_scrape = f'{url}{page}'
                        immobiliare_info = scrape_url_immobiliare(url_to_scrape)
                        
                        if immobiliare_info is not None:
                            all_data.extend(immobiliare_info)

                    if all_data:
                        df = pd.DataFrame(all_data)
                        df.to_csv('Immobiliare/immobiliare_clean.csv', index=False)
                        logging.debug("Immobiliare data saved to CSV")

            else:
                logging.error(f"Failed to scrape {url}. Status code: {response.status_code}")
                return None

        else:
            logging.error(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        return None