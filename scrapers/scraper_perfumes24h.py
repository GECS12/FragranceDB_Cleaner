import sys
import os
import re
import sqlite3
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
from webdriver_manager.chrome import ChromeDriverManager
from db_utils_new import insert_or_update_fragrance, create_table, print_database_contents

def extract_price(price_element):
    text = price_element.text.strip()
    actual_price = re.sub(r'[^\d,\.]', '', text)
    return float(actual_price.replace(',', '.')) if actual_price else None

def extract_name_and_quantity(full_name):
    match = re.search(r"(.+?)\s(\d+)\s*ML", full_name, re.IGNORECASE)
    if match:
        name = match.group(1).strip()
        quantity = int(match.group(2).strip())
        return name, quantity

    quantity_match = re.findall(r"(\d+)", full_name)
    if quantity_match:
        quantity = int(quantity_match[-1].strip())
        name = re.sub(r"\s*\d+\s*ML?", "", full_name, flags=re.IGNORECASE).strip()
        return name, quantity

    print(f"No quantity found for {full_name}. Defaulting quantity to 0.")
    return full_name.strip(), 0

def format_name(name):
    words = name.split()
    special_words = {"EDT", "EDP", "EDC"}
    formatted_words = [word.capitalize() if word not in special_words else word for word in words]
    return ' '.join(formatted_words)

def scroll_to_bottom(driver):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = 0
    retries = 0
    while retries < 5:
        body.send_keys(Keys.END)
        time.sleep(2)  # Adjust delay as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height
            retries = 0  # Reset retries if height increased
        else:
            retries += 1
        print(f"Scrolled to {new_height}, Page height: {last_height}")

def scrape_page(driver, perfume, db_name, table_name, website):
    print("Start scraping page")
    scroll_to_bottom(driver)
    cards = driver.find_elements(By.CLASS_NAME, 'dfd-card')
    print(f"Found {len(cards)} cards on the page.")
    for card in cards:
        try:
            brand = card.find_element(By.CLASS_NAME, 'dfd-card-brand').text
            title = card.find_element(By.CLASS_NAME, 'dfd-card-title').text
            price_element = card.find_element(By.CLASS_NAME, 'dfd-card-price--sale')
            price = extract_price(price_element)
            link = card.find_element(By.CLASS_NAME, 'dfd-card-link').get_attribute('href')
            extra = card.find_element(By.CLASS_NAME, 'dfd-card-extra1').get_attribute('title')

            type_mapping = {
                'eau de toilette': 'EDT',
                'eau de parfum': 'EDP',
                'parfum': 'Parfum',
                'elixir': 'Elixir'
            }
            type_found = None
            for type_name, type_short in type_mapping.items():
                if type_name in extra.lower():
                    type_found = type_short
                    break

            name, quantity = extract_name_and_quantity(title)
            if type_found:
                name_with_type = f"{name} {type_found}"
            else:
                name_with_type = name

            print(f"Name: {name_with_type}, Quantity: {quantity}, Type: {type_found}")
            formatted_name = format_name(name_with_type)
            print(f"Formatted Name: {formatted_name}")

            print(f"Inserting fragrance: {formatted_name}, Price: {price}, Quantity: {quantity}, Link: {link}, Website: {website}")
            insert_or_update_fragrance(db_name, table_name, formatted_name, price, quantity, link, website)
        except Exception as e:
            print(f"Error processing card: {e}")

def scrape_perfumes24h(perfume, db_name, table_name):
    website = "Perfumes24h"
    base_url = "https://perfumes24h.com"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented to run non-headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(base_url)
        print(f"Opened {base_url} successfully.")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.txt_buscar'))
        )
        print("Found search box.")
        search_box.clear()
        search_box.send_keys(perfume)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for the search results to load

        filter_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.dfd-btn-term-filter[dfd-value-term="Perfumes"]'))
        )
        print("Found filter box.")
        filter_box.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dfd-results')))
        print("Found results element.")

        #print("Database contents before scraping:")
        #print_database_contents(db_name, table_name)

        scrape_page(driver, perfume, db_name, table_name, website)

        #print("Database contents after scraping:")
        #print_database_contents(db_name, table_name)

    except ElementNotInteractableException as e:
        print(f"Element not interactable: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    table_name = 'Perfumes24h'
    db_name = 'db_test'
    create_table(db_name, table_name)

    fragrances = ['Abercrombie & fitch', 'Acqua di parma', 'Acqua di selva', 'Adidas', 'Adolfo domínguez', 'Afnan', 'Agua de sevilla', 'Aigner', 'Alvarez gomez', 'Alyssa ashley', 'Amouage', 'Angel schlesser', 'Annayake', 'Antonio banderas', 'Aramis', 'Armaf', 'Armand basi', 'Armani', 'Atkinsons', 'Axe', 'Azzaro', 'Baldessarini', 'Banani', 'Basi', 'Benetton', 'Bentley', 'Biagiotti', 'Bien-etre', 'Blood concept', 'Boss', 'Boucheron', 'Brummel', 'Bruno banani', 'Bultaco', 'Bvlgari', 'Cacharel', 'Calvin klein\t', 'Carolina herrera', 'Cartier', 'Caudalie', 'Cavalli', 'Cerruti', 'Chanel', 'Christian dior', 'Clean', 'Clinique', 'Coach', 'Coquette', 'Coronel tapiocca', 'Couture', 'Creed', 'Cristiano ronaldo', 'Crossmen\n', 'Cuba', 'David beckham', 'Davidoff', 'Diesel', 'Dior', 'Dkny', 'Dolce & gabbana', 'Domínguez', 'Don algodon', 'Dsquared2', 'Duck', 'Dunhill', 'El ganso', 'Emanuel ungaro', 'Emporio armani', 'Escentric molecules', 'Estée lauder', 'Etro', 'Euroluxe', 'F.c. barcelona', 'Faberge', 'Façonnable', 'Ferrari', 'Franck olivier', 'Frozen', 'Gaultier', 'Geoffrey beene', 'Giorgio armani', 'Giorgio beverly', 'Givenchy', 'Guerlain', 'Guess', 'Guy laroche', 'Hackett london', 'Halloween', 'Halston', 'Hannibal laguna', 'Heno de pravia', 'Hermès', 'Herrera', 'Hilfiger', 'Hollister', 'Hugo boss', 'Iceberg', 'Instituto español', 'Issey miyake', 'Jacomo', "Jacq's", 'Jacques bogart', 'Jaguar', 'Jean paul gaultier', 'Jesús del pozo', 'Jil sander', 'Jimmy choo', 'Jo malone', 'John varvatos', 'Joop!', 'Juicy couture', 'Juliette has a gun', 'Karl lagerfeld', 'Kenzo', "L'occitane", 'Lacoste', 'Lalique', 'Lamborghini', 'Lanvin', 'Laroche', 'Lattafa', 'Lauder', 'Laura biagiotti', 'Lauren', 'Legrain', 'Lempicka', 'Loewe', 'Lolita lempicka', 'Luxana', 'Mancera paris', 'Mandarina duck', 'Marbert', 'Mauboussin', 'Mercedes-benz\n\n', 'Ministry of oud', 'Missoni', 'Miyake', 'Monotheme', 'Montale', 'Montblanc', 'Moschino', 'Mugler', 'Narciso rodríguez', 'Natural honey', 'Nautica', 'Nike', 'Nikos', 'Oscar de la renta', 'Pacha ibiza', 'Paco rabanne', 'Paloma picasso', 'Pepe jeans', 'Perry ellis', 'Pertegaz', 'Philipp plein', 'Playboy', 'Police', 'Prada', 'Puig', 'Quorum', 'Rabanne', 'Ralph lauren', 'Rasasi', 'Real madrid', 'Real madrid c.f.', 'Reebok', 'Roberto cavalli', 'Rochas', 'Rodríguez', 'Salvatore ferragamo', 'Saphir', 'Scalpers', 'Schlesser', 'Serge lutens', 'Sergio tacchini', 'Sisley', 'Sportman', 'Springfield', 'Swiss arabian', 'Tabac original\n', 'Ted lapidus', 'Thierry mugler', 'Tom ford', 'Tommy hilfiger', 'Tous', 'Trussardi', 'United colors of benetton', 'Valentino', 'Van cleef & arpels', 'Varon dandy', 'Versace', 'Victor', 'Victorinox', 'Victorio & lucchino', 'Viktor & rolf', 'Xerjoff', 'Yacht man', 'Yves saint laurent', 'Zadig & voltaire', '4711']


    scrape_perfumes24h(fragrances[0], db_name, table_name)
    subprocess.call("TASKKILL /f /IM CHROME.EXE")
