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
                # log(f"Found item: {item_name} with price: {price} on {site_name}")
            else:
                if not item_name_elem:
                    log(f"Missing item name on {site_name} at URL: {url}")
                if not price_elem:
                    log(f"Missing price on {site_name} at URL: {url}")
                log(f"Stopping scrape for {site_name} due to missing data.")
                return items, prices  # Return whatever data was collected so far

        log(f"Found {len(product_elements)} products on {site_name} page {page}")
        page += 1

    log(f"Finished scraping {site_name}. Found total of {len(items)} items.")
    return items, prices

# Function to compare prices and find best prices
def find_best_prices(items, *price_lists):
    combined_data = {}

    for site_index, prices in enumerate(price_lists, start=1):
        for item, price in zip(items, prices):
            if item not in combined_data:
                combined_data[item] = {'Price': price, 'Store': f'Site {site_index}'}
            else:
                if price < combined_data[item]['Price']:
                    combined_data[item]['Price'] = price
                    combined_data[item]['Store'] = f'Site {site_index}'

    return combined_data

# List of site URLs
sites = [
    'https://www.wootware.co.za/computer-hardware?p=',
    'https://www.incredible.co.za/products/gaming/components?p=',
    'https://www.evetech.co.za/search/components?p='
]

# Start scraping
start_time = time.time()
data = []

for url in sites:
    items, prices = scrape_site(url)
    data.append((items, prices))

end_time = time.time()
log(f"Scraping completed in {end_time - start_time:.2f} seconds")

# Output counts
for url, (items, prices) in zip(sites, data):
    site_name = urlparse(url).hostname
    log(f"Count of items found on {site_name}: {len(items)} items")

# Unpack data for comparison
item_lists, price_lists = zip(*data)

# Compare prices and find best prices
combined_data = find_best_prices(item_lists[0], *price_lists)

# Convert combined data to DataFrame
df = pd.DataFrame([
    [item, data['Price'], data['Store']]
    for item, data in combined_data.items()
], columns=['Item', 'Price', 'Store'])

# Save to Excel
excel_file = 'best_prices.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    df.to_excel(writer, sheet_name='Best Prices', index=False)

log(f"Best prices have been saved to {excel_file}")
