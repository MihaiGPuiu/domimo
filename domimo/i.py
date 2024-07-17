from bs4 import BeautifulSoup
import requests

# This list will store the industry names
all_ind = []

def scraper(url):
    try:
        # Requesting the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Successfully fetched the URL: {url}")
        
        # Parsing the webpage content
        soup = BeautifulSoup(response.content, "html.parser")
        print("Successfully parsed the webpage content.")
        
        # Finding all the elements with the specific class
        ind = soup.find_all("ul", class_="MuiList-root MuiList-padding IndustrySelector-industryList mui-1ontqvh")
        print(f"Found {len(ind)} elements with the specified class.")
        
        return ind
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

def get_contents():
    url = "http://proff.se"
    page_contents = scraper(url)

    if page_contents:
        # Extracting text from each element and adding it to the list
        for elem in page_contents:
            all_ind.append(elem.get_text().strip())
        print(f"Successfully extracted text from {len(page_contents)} elements.")
    else:
        print("No content found on the page.")
    return all_ind

if __name__ == "__main__":
    industries = get_contents()
    print("Final extracted industries:", industries)
