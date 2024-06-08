import os
import pandas as pd
import db_utils
from datetime import datetime

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()

def scrape_to_db(fragrances, db_name, table_name):
    # Ensure the Quantity column is numeric and remove decimals if not needed
    def clean_quantity(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        try:
            return int(float(value))
        except ValueError:
            return value

    # Apply cleaning function
    fragrances['Quantity (ml)'] = fragrances['Quantity (ml)'].apply(clean_quantity)

    # Debugging: Print out the Quantity (ml) values before conversion
    #print("Quantities before conversion:")
    #print(fragrances['Quantity (ml)'])

    # Convert Quantity (ml) to integer type if possible
    fragrances['Quantity (ml)'] = pd.to_numeric(fragrances['Quantity (ml)'], downcast='integer', errors='coerce')

    # Debugging: Print out the DataFrame to ensure it's correct
    #print("Fragrances DataFrame before insertion:")
    #print(fragrances)

    # Debugging: Print out the data types of the DataFrame columns
    #print("Data types of the DataFrame columns:")
    #print(fragrances.dtypes)

    db_utils.create_table(db_name, table_name)
    fragrances_tuples = [tuple(row) for row in fragrances[
        ['Brand', 'Fragrance Name', 'Quantity (ml)', 'Price (€)', 'Link', 'Website']].to_records(index=False)]

    # Debugging: Print out the tuples to be inserted
    #print("Tuples to be inserted into the database:")
    #for fragrance in fragrances_tuples:
        #print(fragrance)

    db_utils.insert_multiple_fragrances(db_name, table_name, fragrances_tuples)

    # Print the confirmation message
    print(f"Process Complete:\nDB: {db_name}\nTable: {table_name}\nTotal Fragrances Inserted: {len(fragrances_tuples)}")


def scrape_to_excel(fragrances, base_path, scraper_name):
    timestamp = datetime.now().strftime("%d_%b_%Y %H" + "h" "%M" + "m")
    filename = f'{scraper_name} on {timestamp}.xlsx'
    # Join the base path directly with the filename
    full_path = os.path.join(base_path, filename)
    os.makedirs(base_path, exist_ok=True)  # Ensure base_path directory exists
    fragrances.to_excel(full_path, index=False)
    print(filename + " has been saved in " + full_path)

def standardize_names(string):
    # Define the words to exclude from capitalization
    exclude_words = {"edt", "edp", "edc"}

    # Split the string into words
    words = string.split()

    # Capitalize each word except the ones in the exclude list
    standardized_words = [
        word.upper() if word.lower() in exclude_words else word.capitalize()
        for word in words
    ]

    # Join the words back into a single string
    return ' '.join(standardized_words)
