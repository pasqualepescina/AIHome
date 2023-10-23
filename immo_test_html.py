import logging
import pandas as pd
from bs4 import BeautifulSoup
import requests

base_url = 'https://www.immobiliare.it/vendita-case/milano/?pag=1'
logging.debug("Parsing the content using BeautifulSoup")
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Print the entire HTML response
#print(soup.prettify())

# Save the HTML response to an HTML file
with open('response_immo.html', 'w', encoding='utf-8') as html_file:
    html_file.write(soup.prettify())