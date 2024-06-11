import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    marca_filter = driver.find_element(By.CSS_SELECTOR, 'div.filter-options-item.filter-options-item-brand_mass .filter-options-title')
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
        print(brand_name, brand_url)

    # Close the driver
    driver.quit()
    return brand_urls

#get_brand_urls()

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
    return 0

# Function to clean fragrance name
def clean_fragrance_name(fragrance_name, brand_name):
    website_fragrance_names =  []
    brand_removed_names = []
    final_cleaned_names = []
    website_fragrance_names.append(fragrance_name)
    # Remove brand name case insensitively
    brand_name_regex = re.compile(re.escape(brand_name), re.IGNORECASE)
    fragrance_name = brand_name_regex.sub('', fragrance_name).strip()
    brand_removed_names.append(fragrance_name)
    #print(fragrance_name)
    # Replace case insensitive Eau de Toilette, Eau de Parfum, Eau de Cologne
    fragrance_name = re.sub(r'eau de toilette', 'EDT', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'eau de parfum', 'EDP', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'eau de cologne', 'EDC', fragrance_name, flags=re.IGNORECASE)
    # Remove quantity (e.g., 100ml or 75VAP)
    parts = fragrance_name.split()
    cleaned_parts = [part for part in parts if not ('ml' in part.lower() or 'vap' in part.lower())]
    cleaned_name = ' '.join(cleaned_parts)
    final_cleaned_names.append(cleaned_name)
    return cleaned_name

# Function to scrape fragrance data
def scrape_fragrance_data(brand_url_tuple):
    brand_name, brand_url = brand_url_tuple
    driver.get(brand_url)

    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.item.product.product-item")))
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

        #print(aux_functions.standardize_names(aux_functions.standardize_brand_name(brand_name)))
        #print(aux_functions.standardize_names(cleaned_fragrance_name))

    return data

# Hardcoded brand URLs for testing
#brands_urls = [
    #("Armand basi", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8521"),
    #("Guy Laroche", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8709"),
    #("Helena Rubinstein", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8626"),
#     ("James Bond 007", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8627"),
#     ("Lolita lempicka", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8686"),
#     ("Ach Brito", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6014"),
#     ("Angel schlesser", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8272"),
#     ("Antonio banderas", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6018"),
#     ("Aramis", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6019"),
#     ("Azzaro", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6021"),
#     ("B.U.", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6022"),
#     ("Balenciaga", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6023"),
#     ("Bentley", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6026"),
#     ("Biotherm Homme", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6029"),
#     ("Bottega Veneta", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6030"),
#     ("Boucheron", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6031"),
#     ("Britney spears", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6032"),
#     ("Bulgari", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6033"),
#     ("Burberry", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6034"),
#     ("Cacharel", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6035"),
#     ("Calvin klein", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6036"),
#     ("Carolina Herrera", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6037"),
#     ("Cerruti", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8266"),
#     ("Chanel", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8422"),
#     ("Chloé", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6039"),
#     ("Clinique", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6042"),
#     ("Coach", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6044"),
#     ("Davidoff", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6050"),
#     ("Diesel", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6052"),
#     ("Dkny", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6053"),
#     ("Dolce gabbana", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6054"),
#     ("Dsquared2", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6055"),
#     ("Dunhill", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6056"),
#     ("Elizabeth arden", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6058"),
#     ("Emporio armani", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6059"),
#     ("Escada", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6061"),
#     ("Estee lauder", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6062"),
#     ("Ferrari", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8271"),
#     ("Gianfranco ferre", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6068"),
#     ("Giorgio armani", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6069"),
#     ("Givenchy", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6071"),
#     ("Gucci", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6072"),
#     ("Guerlain", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8448"),
#     ("Halloween", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8066"),
#     ("Heno de Pravia", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8195"),
#     ("Hermes", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6074"),
#     ("Hugo boss", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6075"),
#     ("Issey miyake", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6076"),
#     ("Jacadi", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8023"),
#     ("Jean-paul gaultier", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6079"),
#     ("Jimmy Choo", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6082"),
#     ("Juicy Couture", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6084"),
#     ("Kenzo", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6086"),
#     ("Lacoste", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6091"),
#     ("Lancome", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6094"),
#     ("Lanvin", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6095"),
#     ("Laura biagiotti", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6096"),
#     ("Marc Jacobs", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6098"),
#     ("Michael kors", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6102"),
#     ("Missoni", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8410"),
#     ("Miu Miu", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6103"),
#     ("Mont blanc", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6105"),
#     ("Moschino", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6106"),
#     ("Narciso Rodriguez", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6108"),
#     ("Nike", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6110"),
#     ("Nina ricci", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6111"),
#     ("Nivea Men", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6113"),
#     ("P.gres", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6115"),
#     ("Paco Rabanne", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6116"),
#     ("Prada", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6118"),
#     ("Ralph lauren", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6120"),
#     ("Roberto cavalli", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6121"),
#     ("Rochas", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6122"),
#     ("Salvatore ferragamo", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6124"),
#     ("Sensai", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6125"),
#     ("Shakira", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6126"),
#     ("Shiseido", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6127"),
#     ("Sisley", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6129"),
#     ("Thierry Mugler", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6136"),
#     ("Tiffany & Co.Parfum", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6137"),
#     ("Tom Ford", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6138"),
#     ("Tommy Hilfiger", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6139"),
#     ("Tous", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6140"),
#     ("Trussardi", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6141"),
#     ("Valentino", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6142"),
#     ("Versace", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6145"),
#     ("Victorio & Lucchino", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6146"),
#     ("Viktor & Rolf", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6147"),
#     ("Women secret", "https://mass-perfumarias.pt/perfumes.html?brand_mass=7898"),
#     ("Yves saint laurent", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6149"),
#     ("Zadig & Voltaire", "https://mass-perfumarias.pt/perfumes.html?brand_mass=6150"),
#     ("Mandarina Duck", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8681"),
#     ("Nikos", "https://mass-perfumarias.pt/perfumes.html?brand_mass=8688"),
    # Add more as needed
#]

brands_urls = get_brand_urls()

# Scrape data for each brand
all_data = []
for brand_url_tuple in brands_urls:
    all_data.extend(scrape_fragrance_data(brand_url_tuple))

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Display DataFrame
#print(df)

# Save to CSV or Excel if needed
df.to_excel('fragrance_data.xlsx', index=False)

# Using aux_functions to save to database
db_utils.create_table('PT_fragrances','MassPerfumarias')
aux_functions.scrape_to_db(df, 'PT_fragrances', 'MassPerfumarias')

# Close the WebDriver
driver.quit()
subprocess. call("TASKKILL /f /IM CHROME.EXE")