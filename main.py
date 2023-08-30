import requests
from bs4 import BeautifulSoup
import logging
import os
import json
import pandas as pd
from scrape_master_url import scrape_url_master_tecnocasa, save_to_txt
from scrape_html_childs import scrape_html_files,scrape_multiple_urls

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a folder named "Tecnocasa" if it doesn't exist
output_folder = 'Tecnocasa'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# MASTER URL TO SCRAPE AND GET ALK THE OTHERS
url_to_scrape = 'https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html'

# Scrape the data
scraped_annuncio_items = scrape_url_master_tecnocasa(url_to_scrape)

# Change the current working directory to the output folder
os.chdir(output_folder)
# Save the scraped data to a text file
if scraped_annuncio_items is not None:
    file_path = 'urls_to_scrape_tecnocasa.txt'
    save_to_txt(file_path, scraped_annuncio_items)
else:
    logging.warning("Failed to scrape or no data found.")

# File containing the URLs to scrape
urls_file_path = 'urls_to_scrape_tecnocasa.txt'

# Scrape data from the listed URLs and create files for each URL
scrape_multiple_urls(urls_file_path)
html_files_path = r"C:\Users\pesci\OneDrive\Desktop\AIHome\AIHome\Tecnocasa"
# Get a list of all the files in the directory
html_files = [os.path.join(html_files_path, file) for file in os.listdir(html_files_path) if file.endswith(".html")]

# Call the scrape_html_files function

# Loop through the URLs and scrape data from each one
results_scrapper = scrape_html_files(html_files)

# Combine the JSON data from all files into a single dictionary
combined_data = {}
for data in results_scrapper:
    for key, value in data.items():
        combined_data.setdefault(key, []).extend(value)

# Create a DataFrame directly from the combined_data dictionary
df = pd.DataFrame(combined_data)

# Drop duplicate rows
df.drop_duplicates(inplace=True)

    

