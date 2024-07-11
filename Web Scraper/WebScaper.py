import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def scrape_site(base_url):
    items = []
    prices = []
    site_name = urlparse(base_url).hostname  # Get the site name from the URL
    log(f"Starting to scrape {site_name}")

    page = 1
    while True:
        url = f"{base_url}{page}"
        log(f"Fetching URL: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_elements = soup.select('.item')  # Update this selector based on the actual site's HTML structure
        if not product_elements:
            log(f"No more products found on {site_name}. Ending scrape.")
            break

        for product in product_elements:
            item_name_elem = product.select_one('.product-name a')  # Update this selector based on the actual site's HTML structure
            price_elem = product.select_one('.price')  # Update this selector based on the actual site's HTML structure
            
            if item_name_elem and price_elem:
                item_name = item_name_elem.text.strip()
                price = price_elem.text.strip()
                items.append(item_name)
                prices.append(float(price.replace('R', '').replace(',', '')))
            else:
                if not item_name_elem:
                    log(f"Missing item name on {site_name} at URL: {url}")
                if not price_elem:
                    log(f"Missing price on {site_name} at URL: {url}")
                log(f"Stopping scrape for {site_name} due to missing data.")
                return items, prices  # Return whatever data was collected so far

        log(f"Found {len(product_elements)} products on {site_name} page {page}")
        page += 1
        time.sleep(1)  # Add a short delay to be kind to the server

    log(f"Finished scraping {site_name}. Found total of {len(items)} items.")
    return items, prices

# Main function to scrape Wootware
def main():
    # URL for Wootware
    wootware_url = 'https://www.wootware.co.za/computer-hardware?p='

    # Start scraping Wootware
    start_time = time.time()
    items, prices = scrape_site(wootware_url)
    end_time = time.time()

    # Output counts
    log(f"Count of items found on Wootware: {len(items)} items")

    # Convert data to DataFrame
    df = pd.DataFrame({
        'Item': items,
        'Price': prices
    })

    # Save to Excel
    excel_file = 'wootware_prices.xlsx'
    df.to_excel(excel_file, index=False)

    log(f"Prices from Wootware have been saved to {excel_file}")
    log(f"Scraping completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
