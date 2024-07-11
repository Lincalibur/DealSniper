import pandas as pd

# Function to compare prices across Excel sheets and find best prices
def compare_prices(excel_file, final_sheet_name='FinalSheet'):
    try:
        df = pd.read_excel(excel_file, sheet_name=None)
        sheets = list(df.keys())
        if len(sheets) < 2:
            print("Insufficient sheets to compare prices.")
            return
        
        # Compare prices and find best prices
        best_prices = {}
        for sheet_name in sheets:
            if sheet_name != final_sheet_name:
                data = df[sheet_name]
                for index, row in data.iterrows():
                    product = row['Product']
                    price = row['Price']
                    if product not in best_prices or price < best_prices[product]['Price']:
                        best_prices[product] = {'Sheet': sheet_name, 'Price': price}
        
        # Convert best prices to DataFrame and save to final sheet
        best_prices_df = pd.DataFrame(best_prices.values(), index=best_prices.keys())
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
            best_prices_df.to_excel(writer, sheet_name=final_sheet_name)
        
        print(f"Best prices saved to '{excel_file}', Sheet: '{final_sheet_name}'")
    except Exception as e:
        print(f"Error comparing prices: {e}")

# Example usage:
if __name__ == "__main__":
    excel_file = 'products_data.xlsx'  # Specify your Excel file
    compare_prices(excel_file)
