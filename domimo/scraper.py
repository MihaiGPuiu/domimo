import logging
import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping_log.txt', mode='w'),  # Write logs to a file
        logging.StreamHandler(sys.stdout)  # Output logs to the terminal
    ]
)

# Initialize fake user agent
ua = UserAgent()
HEADERS = {'User-Agent': ua.random}

def names_prices(url):
    logging.info(f"Fetching data from URL: {url}")
url="https://residentialist.ro/apartamente-vanzare/bucuresti"

response = requests.get(url, headers=HEADERS)
logging.debug(f"Response status code: {response.status_code}")

if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        