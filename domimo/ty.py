import requests
from bs4 import BeautifulSoup
import pandas as pd

all_title = []
all_det = []
all_href = []
all_img = []

def scraper():
    for num in range(1, 3):  # Adjusted to 2 pages for testing, increase as needed
        url = f"https://www.olx.ro/imobiliare/?currency=EUR&page={num}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Scrape titles and href links
            elems = soup.find_all("a", class_="css-z3gu2d")
            for e in elems:
                title_elem = e.find("h6", class_="css-1wxaaza")
                if title_elem:
                    title = title_elem.get_text().strip()
                    href = e.get('href')
                    
                    if href.startswith("/d/"):
                        href = "https://www.olx.ro" + href
                        
                        # Find the image URL within the listing
                        img_urls = []
                        img_elems = e.find_all('div', class_='swiper-zoom-container')
                        for img_elem in img_elems:
                            img_tag = img_elem.find('img')
                            if img_tag and 'src' in img_tag.attrs:
                                img_urls.append(img_tag['src'])
                        
                        img_url = img_urls[0] if img_urls else "n/a"
                        all_img.append(img_url)
                    
                    if href and title and href not in all_href:
                        all_title.append(title)
                        all_href.append(href)
                        
                        # Initialize price as "n/a" in case it's not found
                        price = "n/a"
                        
                        # Search for price within the same listing container
                        price_elem = e.find_next_sibling("p", class_="css-13afqrm")
                        if price_elem:
                            price = price_elem.get_text().replace("Prețul e negociabil", "").strip()
                        
                        all_det.append(price)
            
            print(f"Scraped a total of {len(all_title)} titles, {len(all_det)} prices, and {len(all_href)} links")
        
        else:
            print(f"Failed to retrieve page {num}. Status code: {response.status_code}")

scraper()

# Ensure all lists have the same length
min_length = min(len(all_title), len(all_det), len(all_href), len(all_img))
all_title = all_title[:min_length]
all_det = all_det[:min_length]
all_href = all_href[:min_length]
all_img = all_img[:min_length]

# Create DataFrame
df = pd.DataFrame({
    "Title": all_title,
    "Price": all_det,
    "Links": all_href,
    "Image": all_img
})

df.to_excel("numaidamuie.xlsx", index=False)
