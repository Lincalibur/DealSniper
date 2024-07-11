import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to scrape a web page and save prices to Excel
def scrape_and_save(url, excel_file):
    headers = {
        'User-Agent': 'Your User Agent String',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Extracting product names and prices
        products = soup.find_all('div', class_='product')
        data = []
        for product in products:
            name = product.find('h2').text.strip()
            price = product.find('span', class_='price').text.strip()
            data.append({'Product': name, 'Price': price})
        
        # Check if Excel file exists, create if not
        if not os.path.exists(excel_file):
            df_empty = pd.DataFrame()
            df_empty.to_excel(excel_file, index=False)
        
        # Append to existing or newly created Excel sheet
        df = pd.DataFrame(data)
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=url, index=False)
        
        print(f"Data saved to '{excel_file}', Sheet: '{url}'")
    else:
        print(f"Failed to retrieve data from {url}")

# Example usage:
if __name__ == "__main__":
    url = 'https://www.wootware.co.za/computer-hardware?p='  # Replace with your URL
    excel_file = 'products_data.xlsx'  # Specify your Excel file
    scrape_and_save(url, excel_file)
