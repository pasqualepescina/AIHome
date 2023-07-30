import requests
from bs4 import BeautifulSoup

def scrape_annuncio_items(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the web page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the listings with class "annuncio-item" on the page
            annuncio_items = soup.find_all()

            # Return the list of scrapped data
            return annuncio_items

        else:
            print(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error while scraping {url}: {str(e)}")
        return None

def save_to_txt(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(str(item) + "\n")
                file.write("-" * 40 + "\n")

        print(f"Scraped data saved to {file_path}")

    except Exception as e:
        print(f"Error while saving to {file_path}: {str(e)}")

# URL to scrape
url_to_scrape = 'https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html'

# Scrape the data
scraped_annuncio_items = scrape_annuncio_items(url_to_scrape)

# Save the scrapped data to a text file
if scraped_annuncio_items is not None:
    file_path = 'scraped_data_tecnocasa.txt'
    save_to_txt(file_path, scraped_annuncio_items)
else:
    print("Failed to scrape or no data found.")
