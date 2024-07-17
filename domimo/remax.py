import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import re

def scrape_olx_listings():
    # Create a user agent
    ua = UserAgent()
    HEADERS = {'User-Agent': ua.random}

    # Initialize lists to store data
    title_list = []
    price_list = []
    surface_list = []
    listing_urls = []
    image_links = []

    # Set to keep track of processed URLs to avoid duplication
    processed_urls = set()

    # Function to extract data from a single listing
    def process_listing_url(full_url):
        try:
            listing_response = requests.get(full_url, headers=HEADERS)
            if listing_response.status_code == 200:
                listing_soup = BeautifulSoup(listing_response.content, 'html.parser')
                
                # Find all image containers
                image_containers = listing_soup.find_all('div', class_='swiper-slide')
                
                # Initialize list to store image URLs for current listing
                listing_image_links = []
                
                # Extract image URLs from each container
                for container in image_containers:
                    img_tag = container.find('img')
                    if img_tag and img_tag.has_attr('src'):
                        image_url = img_tag['src']
                        listing_image_links.append(image_url)
                
                # Concatenate image URLs with commas and add to main list
                if listing_image_links:
                    return ", ".join(listing_image_links)
                else:
                    return "N/A"
        except Exception as e:
            print(f"Error processing listing URL {full_url}: {str(e)}")
            return "N/A"

    # Loop through the pages
    for num in range(1, 25):  # Adjust the range as needed
        url = f"https://www.olx.ro/imobiliare/?page={num}"
        response = requests.get(url, headers=HEADERS)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract and append titles
            descriptions = soup.find_all("h6", class_="css-1wxaaza")
            for desc in descriptions:
                title_list.append(desc.get_text(strip=True))
            
            # Extract and append surfaces
            surfaces = soup.find_all("span", class_="css-643j0o")
            for surface in surfaces:
                # Extract numeric part before "m²"
                surface_text = surface.get_text(strip=True)
                match = re.search(r'(\d+(?:\.\d+)?)\s*m²', surface_text)
                if match:
                    surface_list.append(match.group(1))
                else:
                    surface_list.append("N/A")
            
            # Extract and append prices
            prices = soup.find_all("p", class_="css-13afqrm")
            for price in prices:
                price_text = price.get_text(strip=True)
                price_list.append(price_text)
            
            # Extract listing URLs
            listings = soup.find_all("a", class_="css-z3gu2d")
            for listing in listings:
                link = listing.get('href')
                if link:
                    if link.startswith("http"):
                        full_url = link
                    elif "www.storia.ro" in link:
                        full_url = link
                    else:
                        full_url = "https://www.olx.ro" + link
                    
                    # Check if the URL has already been processed
                    if full_url not in processed_urls:
                        processed_urls.add(full_url)
                        listing_urls.append(full_url)
                        
                        # Extract image links for the current listing URL
                        image_links.append(process_listing_url(full_url))
            
            # Debugging print
            print(f"Page {num} - Listings processed: {len(listings)}")
            print(f"Page {num} - Titles extracted: {len(title_list)}")
            print(f"Page {num} - Surfaces extracted: {len(surface_list)}")
            print(f"Page {num} - Prices extracted: {len(price_list)}")
            print(f"Page {num} - Listing URLs extracted: {len(listing_urls)}")
            print(f"Page {num} - Image links extracted: {len(image_links)}")
        
        else:
            print(f"Failed to retrieve page {num}")

    return title_list, surface_list, price_list, listing_urls, image_links

# Keep running the script until valid titles are found
while True:
    title_list, surface_list, price_list, listing_urls, image_links = scrape_olx_listings()
    
    # Check if title_list contains only "N/A"
    if all(title == "N/A" for title in title_list):
        print("No valid data found, all titles are 'N/A'. Restarting the script...")
    else:
        break

# Ensure all lists have the same length
max_length = max(len(title_list), len(price_list), len(surface_list), len(listing_urls), len(image_links))
while len(title_list) < max_length:
    title_list.append("N/A")
while len(surface_list) < max_length:
    surface_list.append("N/A")
while len(price_list) < max_length:
    price_list.append("N/A")
while len(listing_urls) < max_length:
    listing_urls.append("N/A")
while len(image_links) < max_length:
    image_links.append("N/A")

# Create a DataFrame from the lists
df = pd.DataFrame({
    "Title": title_list,
    "Surface (m²)": surface_list,
    "Price": price_list,
    "Listing URL": listing_urls,
    "Image URLs": image_links
})

# Save the DataFrame to an Excel file
df.to_excel("listingsvan.xlsx", index=False)

# Print the DataFrame
print(df)
