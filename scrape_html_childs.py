from bs4 import BeautifulSoup
import logging
import json
import requests
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_all_content_from_url(url):
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
            all_child_info = str(soup.findAll())
            return all_child_info

        else:
            logging.error(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        return None

def scrape_multiple_urls(urls_file):
    """
    Scrape data from multiple URLs listed in a file and create files with scraped data.

    Parameters:
        urls_file (str): Path to the file containing the URLs to scrape.

    Returns:
        None
    """
    try:
        with open(urls_file, 'r') as file:
            urls = file.read().splitlines()

        for url in urls:
            # Scrape data from each URL
            data = get_all_content_from_url(url)
            if data:
                # Create a file with the name as the last part of the URL without '.html'
                filename = url.split('/')[-1].replace('.html', '') + '.html'

                # Write the scraped data to the file
                with open(filename, 'w', encoding='utf-8') as output_file:
                    output_file.write(data)

                logging.info(f"Data scraped from {url} and saved to {filename}")

    except Exception as e:
        logging.error(f"Error while reading URLs from {urls_file}: {str(e)}")

def extract_estate_data(soup):
    # Initialize an empty dictionary to store the extracted data
    estate_data = {}
    # Specify the order of occurrence of the tag names

    # Find each occurrence of estate-price, estate-title, estate-subtitle, estate-rooms, estate-surface
    tag_names = ['estate-price', 'estate-title', 'estate-subtitle', 'estate-rooms', 'estate-surface']
    for tag_name in tag_names:
        elements = soup.find_all(lambda tag: tag.name == 'template' and tag.get('slot') == tag_name)
        if elements:
            estate_data[tag_name] = [element.get_text(strip=True) for element in elements]
        else:
            logging.warning(f"Tag '{tag_name}' not found in the HTML content")

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