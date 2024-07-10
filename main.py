# main.py

import config
from modules import html_analyzer

def confirm_elements(url, item_elements, price_elements):
    """
    Displays identified item and price elements and asks for confirmation from the user.

    Args:
    - url (str): URL being analyzed.
    - item_elements (list): List of identified item elements (HTML).
    - price_elements (list): List of identified price elements (HTML).

    Returns:
    - bool: True if confirmed, False otherwise.
    """
    print(f"\nAnalyzing {url}:")
    print("Found potential item elements:")
    for i, item in enumerate(item_elements, start=1):
        print(f"{i}. {item.text.strip()}")

    print("\nFound potential price elements:")
    for i, price in enumerate(price_elements, start=1):
        print(f"{i}. {price.text.strip()}")

    while True:
        choice = input("\nDo you confirm these elements? (yes/no): ").strip().lower()
        if choice == 'yes':
            return True
        elif choice == 'no':
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    urls = [site['url'] for site in config.SITES]  # Read URLs from config.py

    results = html_analyzer.analyze_html(urls)

    for url, (item_elements, price_elements) in results.items():
        if confirm_elements(url, item_elements, price_elements):
            print("Confirmed. Proceeding with scraping...")
            # Add logic to scrape items and prices from websites using confirmed elements
        else:
            print("Confirmation declined. Skipping this site.")

    print("\nAll sites analyzed.")
