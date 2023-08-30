import requests
from bs4 import BeautifulSoup
import logging
import os
import json
import pandas as pd
def extract_estate_data(soup):
    # Initialize an empty dictionary to store the extracted data
    estate_data = {}
    # Specify the order of occurrence of the tag names
    tag_names = ['estate-price', 'estate-title', 'estate-subtitle', 'estate-rooms', 'estate-surface']

    # Find each occurrence of estate-price, estate-title, estate-subtitle, estate-rooms, estate-surface
    tag_names = ['estate-price', 'estate-title', 'estate-subtitle', 'estate-rooms', 'estate-surface']
    for tag_name in tag_names:
        elements = soup.find_all(lambda tag: tag.name == 'template' and tag.get('slot') == tag_name)
        if elements:
            estate_data[tag_name] = [element.get_text(strip=True) for element in elements]
        else:
            logging.warning(f"Tag '{tag_name}' not found in the HTML content")

    return estate_data

    return estate_data

def scrape_html_files(html_files):
    results_json = []

    for file_path in html_files:
        try:
            # Read the content of the HTML file
            with open(file_path, 'r') as file:
                html_content = file.read()

            # Parse the content of the HTML file using BeautifulSoup
            logging.debug(f"Parsing HTML content from file: {file_path}")
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the data from the parsed HTML
            estate_data = extract_estate_data(soup)

            # Create the JSON filename based on the input file path
            json_filename = os.path.splitext(file_path)[0] + ".json"

            # Save the estate_data as a JSON file
            with open(json_filename, "w") as json_file:
                json.dump(estate_data, json_file)

            logging.info(f"Estate data from {file_path} saved to {json_filename}")

            results_json.append(estate_data)

        except Exception as e:
            logging.error(f"Error while scraping {file_path}: {str(e)}")
            results_json.append(None)

    return results_json

html_files_path = r"C:\Users\pesci\OneDrive\Desktop\AIHome\AIHome\Tecnocasa"

# Get a list of all the files in the directory that have the ".html" extension
html_files = [os.path.join(html_files_path, file) for file in os.listdir(html_files_path) if file.endswith(".html")]

# Call the scrape_html_files function to process all HTML files
results_to_json = scrape_html_files(html_files)

# Combine the JSON data from all files into a single dictionary
combined_data = {}
for data in results_to_json:
    for key, value in data.items():
        combined_data.setdefault(key, []).extend(value)

# Create a DataFrame directly from the combined_data dictionary
df = pd.DataFrame(combined_data)

# Drop duplicate rows
df.drop_duplicates(inplace=True)

# Save the DataFrame to CSV
output_csv = os.path.join(html_files_path, "data_clean.csv")
df.to_csv(output_csv, index=False)