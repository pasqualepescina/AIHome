import requests
from bs4 import BeautifulSoup

def scrape_web(urls):
    scraped_data = []
    for url in urls:
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the content of the web page using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Your scraping logic here
                # For demonstration purposes, let's assume we want to scrape all the text from the page.
                # You can modify this part according to your specific scraping needs.
                scraped_text = soup.get_text()
                scraped_data.append(scraped_text)

            else:
                print(f"Failed to scrape {url}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error while scraping {url}: {str(e)}")

    return scraped_data

# Example usage:
urls_to_scrape = ['https://www.immobiliare.it/agenzie-immobiliari/224672/palermo-via-delle-magnolie/?criterio=rilevanza&msclkid=db4e8a7e323117e046d0eec049e4e5ca&utm_source=bing&utm_medium=cpc&utm_campaign=search%7Cagency%7Ccontract%7Cit%7Call%7Cit&utm_term=%2Fagenzie-immobiliari%2F%20agenzia&utm_content=agency%7Ccard%7Ccontract%7Cmunicipality%7Czone%7Cfilter%7Cit%7Call%7Cit%7Cdsa']
scraped_results = scrape_web(urls_to_scrape)

# Print the scraped data from each URL
for i, result in enumerate(scraped_results, 1):
    print(f"Scraped data from URL {i}:")
    print(result)
    print("-" * 40)
