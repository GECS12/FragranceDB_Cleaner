import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import aux_functions  # Assuming aux_functions is the module containing scrape_to_db
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import re
import subprocess
import db_utils
import nest_asyncio

nest_asyncio.apply()


def get_brand_urls():
    # Initialize the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Open the webpage
    driver.get("https://mass-perfumarias.pt/perfumes.html")

    # Wait for the page to load completely
    time.sleep(1)

    # Find the "Marca" filter options title and click it
    marca_filter = driver.find_element(By.CSS_SELECTOR,
                                       'div.filter-options-item.filter-options-item-brand_mass .filter-options-title')
    ActionChains(driver).move_to_element(marca_filter).click().perform()

    # Wait for the options to expand
    time.sleep(1)

    # Now, you can proceed to extract the brands
    brands = driver.find_elements(By.CSS_SELECTOR, 'div.filter-options-item.filter-options-item-brand_mass li.item')
    brand_urls = []
    for brand in brands:
        brand_name = brand.find_element(By.CSS_SELECTOR, 'span.swissup-option-label').text
        brand_url = brand.find_element(By.CSS_SELECTOR, 'a.swissup-aln-item').get_attribute('href')
        brand_urls.append((brand_name, brand_url))

    # Close the driver
    driver.quit()
    return brand_urls


# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


# Function to extract quantity from fragrance name
def extract_quantity(fragrance_name):
    parts = fragrance_name.split()
    for part in parts:
        if 'ml' in part.lower() or 'vap' in part.lower():
            try:
                quantity = int(''.join(filter(str.isdigit, part)))
                return quantity
            except ValueError:
                return 0  # Return 0 if conversion fails

    # Special case: check if the last part is a number
    try:
        quantity = int(parts[-1])
        return quantity
    except ValueError:
        return 0  # Return 0 if no valid quantity found


# Function to clean fragrance name
def clean_fragrance_name(fragrance_name, brand_name):
    # Special cases for brand names
    special_cases = {
        "Angel schlesser": ["Angel Schelesser"],
        "Bulgari": ["Bvlgari"],
        "Dolce gabbana": ["Dolce & Gabbana"],
        "Emporio Armani": ["Giorgio Armani"],
        "Estee Lauder": ["Estée Lauder"],
        "Gianfranco Ferre": ["Gianfranco Ferré"],
        "Hermes": ["Hermès"],
        "Jean-paul gaultier": ["Jean Paul Gaultier"],
        "Lancome": ["Lancôme"],
        "Mont blanc": ["Montblanc"],
        "Tiffany & Co.Parfum": ["Tiffany & Co."]
    }

    # Remove brand name case insensitively, including special cases
    brand_variations = special_cases.get(brand_name, [brand_name])
    for variation in brand_variations:
        brand_name_regex = re.compile(re.escape(variation), re.IGNORECASE)
        fragrance_name = brand_name_regex.sub('', fragrance_name).strip()

    # Replace case insensitive Eau de Toilette, Eau de Parfum, Eau de Cologne
    fragrance_name = re.sub(r'eau de toilette', 'EDT', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'eau de parfum', 'EDP', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'eau de cologne', 'EDC', fragrance_name, flags=re.IGNORECASE)
    # Remove quantity (e.g., 100ml or 75VAP)
    parts = fragrance_name.split()
    cleaned_parts = [part for part in parts if not ('ml' in part.lower() or 'vap' in part.lower())]
    cleaned_name = ' '.join(cleaned_parts)

    # Special case for Trussardi
    if brand_name.lower() == 'trussardi':
        if fragrance_name.lower().startswith('trussardi eau de parfum'):
            cleaned_name = fragrance_name

    return cleaned_name


# Function to scrape fragrance data
async def scrape_fragrance_data(brand_url_tuple):
    brand_name, brand_url = brand_url_tuple
    driver.get(brand_url)

    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.item.product.product-item")))
    except Exception as e:
        print(f"No data found for {brand_name}, moving to next brand.")
        return []

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all fragrance items
    fragrance_items = soup.find_all("li", class_="item product product-item")

    data = []

    for item in fragrance_items:
        # Check if the fragrance is "Esgotado"
        esgotado_tag = item.find("div", class_="stock unavailable")
        if esgotado_tag and "Esgotado" in esgotado_tag.text:
            continue

        # Extract fragrance name
        fragrance_name_tag = item.find("a", class_="product-item-link")
        fragrance_name = fragrance_name_tag.text.strip()

        # Extract quantity
        quantity = extract_quantity(fragrance_name)

        if quantity == 0:
            continue  # Ignore fragrance without quantity in name

        # Clean fragrance name
        cleaned_fragrance_name = clean_fragrance_name(fragrance_name, brand_name)

        # Extract price
        price_tag = item.find("span", class_="price")
        price = price_tag.text.strip().replace('€', '').replace(',', '.').strip() if price_tag else None
        if price is not None:
            try:
                price = float(price)
            except ValueError:
                price = None  # Handle case where conversion to float fails

        # Extract first link
        link = fragrance_name_tag['href']

        # Create data entry
        data.append({
            "Brand": aux_functions.standardize_names(aux_functions.standardize_brand_name(brand_name)),
            "Fragrance Name": aux_functions.standardize_names(cleaned_fragrance_name),
            "Quantity (ml)": quantity,
            "Price (€)": price,
            "Link": link,
            "Website": 'MassPerfumarias'
        })

    return data


# Hardcoded brand URLs for testing
brands_urls = get_brand_urls()

# Scrape data for each brand
all_data = []


async def main():
    tasks = [scrape_fragrance_data(brand_url_tuple) for brand_url_tuple in brands_urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_data.extend(result)


# Run the async main function
asyncio.run(main())

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Display DataFrame
# print(df)

# Save to CSV or Excel if needed
df.to_excel('fragrance_data.xlsx', index=False)

# Using aux_functions to save to database
db_utils.create_table('PT_fragrances', 'MassPerfumarias')
aux_functions.scrape_to_db(df, 'PT_fragrances', 'MassPerfumarias')

# Close the WebDriver
driver.quit()
subprocess.call("TASKKILL /f /IM CHROME.EXE")
