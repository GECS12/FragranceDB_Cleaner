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


#Brand Name Normalizer
BRAND_NAME_MAPPING = {
    'Mugler': 'Thierry Mugler',
    'Armani': 'Giorgio Armani',
    'Abercrombie': 'Abercrombie & Fitch',
    'Dior': 'Christian Dior',
    'Lauren': 'Ralph Lauren',
    'CK': 'Calvin Klein',
    'Arden': 'Elizabeth Arden',
    'Joop': 'Joop!',
    'Paco': 'Paco Rabanne',
    'Gianni Versace': 'Versace',
    'Saint Laurent': 'Yves Saint Laurent',
    'YSL': 'Yves Saint Laurent',
    'Hugo': 'Hugo Boss',
    'Tommy': 'Tommy Hilfiger',
    'Cavalli': 'Roberto Cavalli',
    'Mont blanc': 'Montblanc',
    'Guerlain': 'Guerlain',
    'Hermes': 'Hermès',
    'Viktor and Rolf': 'Viktor & Rolf',
    'Jean Paul': 'Jean Paul Gaultier',
    'Bulgari': 'Bvlgari',
    'Vanderbilt': 'Gloria Vanderbilt',
    'Issey': 'Issey Miyake',
    'Ferragamo': 'Salvatore Ferragamo',
    'Nina': 'Nina Ricci',
    'Rodriguez': 'Narciso Rodriguez',
    'Boss': 'Hugo Boss',
    'Balmain': 'Pierre Balmain',
    'Aramis': 'Aramis',
    'Estee Lauder': 'Estée Lauder',
    'Lancome': 'Lancôme',
    'Lauder': 'Estée Lauder',
    'Kors': 'Michael Kors',
    'Couture': 'Juicy Couture',
    'Annick Goutal': 'Goutal Paris',
    'Beckham': 'David Beckham',
    'Zegna': 'Ermenegildo Zegna',
    'By Kilian': 'Kilian',
    'Comme des Garcons': 'Comme des Garçons',
    'Donna Karan': 'DKNY',
    'Jimmy Choo': 'Jimmy Choo',
    'Malone': 'Jo Malone',
    'Varvatos': 'John Varvatos',
    'Margiela': 'Maison Margiela',
    'Hilfiger': 'Tommy Hilfiger',
    'Lapidus': 'Ted Lapidus',
    'Lagerfeld': 'Karl Lagerfeld',
    'Biagiotti': 'Laura Biagiotti',
    'Duck': 'Mandarina Duck',
    'Gualtier': 'Jean Paul Gaultier',
    'Giorgio Beverly': 'Giorgio Beverly Hills',
    'Jessica Parker': 'Sarah Jessica Parker',
    'Lamborghini': 'Tonino Lamborghini',
    'Lempicka': 'Lolita Lempicka',
    'Puig': 'Antonio Puig',
    'Y.s.laurent': 'Yves Saint Laurent',
    'Y.S.LAURENT': 'Yves Saint Laurent',
    'ABERCROMBIE': 'Abercrombie & Fitch',
    'LAPIDUS': 'Ted Lapidus',
    'VIKTOR Y ROLPH': 'Viktor & Rolph',
    'Viktor and Rolph': 'Viktor & Rolph',
    'Dsquared': 'Dsquared2'

}

def standardize_brand_name(brand_name):
    # Use the dictionary to map the brand name to the standard name if it exists
    return BRAND_NAME_MAPPING.get(brand_name, brand_name)
