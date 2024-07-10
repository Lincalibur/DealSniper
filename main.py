# main.py

import requests
import pandas as pd
import time
from modules.html_analyzer import extract_items_and_prices
from config import WEBSITES

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def scrape_website(url, site_name):
    items = []
    prices = []
    page = 1
    log(f"Starting to scrape {site_name}")

    while True:
        url_with_page = f"{url}{page}"
        log(f"Fetching URL: {url_with_page}")
        response = requests.get(url_with_page)
        if response.status_code != 200:
            log(f"Failed to fetch {url_with_page}. Status code: {response.status_code}")
            break

        items_found, prices_found = extract_items_and_prices(response.text)
        if not items_found or not prices_found:
            log(f"No items or prices found on {site_name} at URL: {url_with_page}")
            break

        items.extend(items_found)
        prices.extend(prices_found)
        log(f"Found {len(items_found)} items on {site_name} page {page}")

        page += 1

    log(f"Finished scraping {site_name}. Found {len(items)} items in total.")
    return items, prices

# Start scraping
start_time = time.time()
data = []

for site in WEBSITES:
    site_name = site['name']
    site_url = site['url']
    items, prices = scrape_website(site_url, site_name)
    data.append((items, prices))

end_time = time.time()
log(f"Scraping completed in {end_time - start_time:.2f} seconds")

# Further processing (comparison, saving to Excel) can be added here

