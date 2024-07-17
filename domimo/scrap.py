import logging
import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
    
    list_remax_name = []
    
    try:
        response = requests.get(url, headers=HEADERS)
        logging.debug(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all("div", class_="property-description")
            for elm in titles:
                list_remax_name.append(elm.get_text(strip=True))  # Strip whitespace from the text
            logging.info(f"Scraped {len(list_remax_name)} apartment names.")
        else:
            logging.error(f"Failed to fetch data from URL: {url} with status code {response.status_code}")
    
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
    
    return list_remax_name

# Example usage:
url = "https://www.remax.ro/vanzare/apartamente/bucuresti-ilfov/bucuresti"
apartment_names = names_prices(url)
for name in apartment_names:
    print(name)
