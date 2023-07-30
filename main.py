import pandas as pd
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

                # Extract all the HTML tags and their corresponding text
                html_labels = [tag.name for tag in soup.find_all()]
                scraped_text = [tag.get_text() for tag in soup.find_all()]

                # Combine the HTML labels and text into a DataFrame
                df = pd.DataFrame({'HTML_Label': html_labels, 'Text': scraped_text})

                # Append the DataFrame to the list of scraped data
                scraped_data.append(df)

            else:
                print(f"Failed to scrape {url}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error while scraping {url}: {str(e)}")

    return scraped_data

# Example usage:
urls_to_scrape = ['https://example.com/page1', 'https://example.com/page2', 'https://example.com/page3']
scraped_results = scrape_web(urls_to_scrape)

# Concatenate the list of DataFrames into a single DataFrame
final_df = pd.concat(scraped_results, ignore_index=True)

# Print the resulting DataFrame
print(final_df)
