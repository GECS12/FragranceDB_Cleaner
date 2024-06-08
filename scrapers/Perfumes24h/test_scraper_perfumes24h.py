import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import nest_asyncio
from datetime import datetime
import db_utils
import aux_functions
import os

nest_asyncio.apply()

def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return ascii_text

def construct_brand_url(brand_name):
    brand_name = normalize_text(brand_name)
    brand_slug = re.sub(r'[^a-z0-9]+', '-', brand_name.lower().replace('&', '-')).strip('-')
    return f"https://perfumes24h.com/perfumes/{brand_slug}/"

def replace_fragrance_type(fragrance_name):
    fragrance_name = re.sub(r'\beau de toilette\b', 'EDT', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'\beau de parfum\b', 'EDP', fragrance_name, flags=re.IGNORECASE)
    fragrance_name = re.sub(r'\beau de cologne\b', 'EDC', fragrance_name, flags=re.IGNORECASE)
    return fragrance_name

def scrape_fragrances(soup, base_url, brand):
    fragrances = []
    print("Started scraping brand: " + brand)
    try:
        products = soup.find_all('div', class_='item_producto')
        for product in products:
            fragrance_name = ""
            price = 0.0
            quantity = 0.0
            link = ""

            brand_name = aux_functions.standardize_names(brand)

            aux_name = product.find('div', class_='tipo_producto').text.strip()
            if aux_name != "":
                fragrance_name = product.find('div', class_='nombre_grupo').text.strip() + " " + aux_name
            else:
                fragrance_name = product.find('div', class_='nombre_grupo').text.strip()

            fragrance_name = replace_fragrance_type(fragrance_name)

            link_tags = product.find_all('a', href=True)
            if len(link_tags) > 1:
                link = link_tags[1]['href']
            if not link.startswith('http'):
                link = base_url + link

            variants = product.find_all('div', class_='item_tamanyo')
            for variant in variants:
                quantity_text = variant.text.strip()

                if quantity_text.lower() == 'set':
                    quantity = 'set'
                else:
                    quantity_match = re.search(r'(\d+)\s*ml', quantity_text, re.IGNORECASE)
                    if quantity_match:
                        quantity = float(quantity_match.group(1))
                        if quantity.is_integer():
                            quantity = int(quantity)
                    else:
                        quantity = 0.0

                price_text = variant.get('data-pp', '0').replace(',', '.')
                price = float(price_text)

                if fragrance_name and price and link:
                    fragrances.append({
                        'Brand': brand_name,
                        'Fragrance Name': fragrance_name,
                        'Quantity (ml)': quantity,
                        'Price (€)': price,
                        'Link': link,
                        'Website': "Perfumes24h"
                    })

    except Exception as e:
        print(f"Error while scraping brand {brand}: {e}")

    df = pd.DataFrame(fragrances)
    return df

async def get_all_brands(url):
    async with aiohttp.ClientSession() as session:
        response = await aux_functions.fetch(session, url)
        soup = BeautifulSoup(response, 'html.parser')
        brands = []
        brand_divs = soup.find_all('div', id=re.compile('^letra_'))
        for brand_div in brand_divs:
            brand_name = brand_div['data-nombre_marca']
            brands.append(brand_name)
    return brands

async def main():
    base_url = "https://perfumes24h.com/"
    brands_url = "https://perfumes24h.com/perfumes/"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    special_urls = {
        'Aguilera': 'https://perfumes24h.com/perfumes/christina-aguilera/',
        'Annayake': 'https://perfumes24h.com/perfumes-11/',
        'Arden': 'https://perfumes24h.com/perfumes/elizabeth-arden/',
        'Banani': 'https://perfumes24h.com/perfumes/bruno-banani/',
        'Basi': 'https://perfumes24h.com/perfumes/armand-basi/',
        'Biagiotti': 'https://perfumes24h.com/perfumes/laura-biagiotti/',
        'Boss': 'https://perfumes24h.com/perfumes/hugo-boss/',
        'Cavalli': 'https://perfumes24h.com/perfumes/roberto-cavalli/',
        'Christian dior': 'https://perfumes24h.com/perfumes/dior/',
        'Couture': 'https://perfumes24h.com/perfumes/juicy-couture/',
        'Cry babies': 'https://perfumes24h.com/perfumes/cry-babies/',
        'Denenes ': 'https://perfumes24h.com/perfumes-4/',
        'Domínguez': 'https://perfumes24h.com/perfumes/adolfo-dominguez/',
        'Duck': 'https://perfumes24h.com/perfumes/mandarina-duck/',
        'Emporio armani': 'https://perfumes24h.com/perfumes/armani/',
        'Escentric molecules': 'https://perfumes24h.com/perfumes/escentric/',
        'Gaultier': 'https://perfumes24h.com/perfumes/jean-paul-gaultier-1/',
        'Giorgio armani': 'https://perfumes24h.com/perfumes/armani/',
        'Gloria vanderbilt': 'https://perfumes24h.com/perfumes/vanderbilt/',
        'Helene fischer': 'https://perfumes24h.com/perfumes/helene-fischer/',
        'Herrera': 'https://perfumes24h.com/perfumes/carolina-herrera/',
        'Hilfiger': 'https://perfumes24h.com/perfumes/tommy-hilfiger/',
        'Hilton': 'https://perfumes24h.com/perfumes/paris-hilton/',
        'Jeanne arthes': 'https://perfumes24h.com/perfumes/jeanne-arthes/',
        'Jessica parker': 'https://perfumes24h.com/perfumes/sarah-jessica-parker/',
        'Jesús del pozo': 'https://perfumes24h.com/perfumes/halloween/',
        'Kardashian': 'https://perfumes24h.com/perfumes/kim-kardashian/',
        'Laroche': 'https://perfumes24h.com/perfumes/guy-laroche/',
        'Lauder': 'https://perfumes24h.com/perfumes/estee-lauder-1/',
        'Lauren': 'https://perfumes24h.com/perfumes/ralph-lauren/',
        'Lempicka': 'https://perfumes24h.com/perfumes/lolita-lempicka/',
        'Liu·jo': 'https://perfumes24h.com/perfumes/liu-jo-1/',
        'Mancera paris': 'https://perfumes24h.com/perfumes/mancera-1/',
        'Mickey mouse': 'https://perfumes24h.com/perfumes/mickey-mouse/',
        'Minnie mouse': 'https://perfumes24h.com/perfumes/minnie-mouse/',
        'Miyake': 'https://perfumes24h.com/perfumes/issey-miyake/',
        'Mugler': 'https://perfumes24h.com/perfumes/thierry-mugler-1/',
        'Rabanne': 'https://perfumes24h.com/perfumes/paco-rabanne/',
        'Real madrid c.f.': 'https://perfumes24h.com/perfumes-2/',
        'Ricci': 'https://perfumes24h.com/perfumes/nina-ricci/',
        'Rodríguez': 'https://perfumes24h.com/perfumes/narciso-rodriguez/',
        'Schlesser': 'https://perfumes24h.com/perfumes/angel-schlesser/',
        'Spiderman': 'https://perfumes24h.com/perfumes/spiderman/',
        'Taylor': 'https://perfumes24h.com/perfumes/elizabeth-taylor/',
        'United colors of benetton': 'https://perfumes24h.com/perfumes/benetton/',
        'Yacht man': 'https://perfumes24h.com/perfumes/yatch-man/',
        'Zaitsev': 'https://perfumes24h.com/perfumes/slava-zaitsev/'
    }

    brands = await get_all_brands(brands_url)
    brand_urls = [(brand, special_urls.get(brand, construct_brand_url(brand))) for brand in brands]

    unique_urls = set()
    unique_brand_urls = []
    duplicates = []

    for brand, url in brand_urls:
        if url not in unique_urls:
            unique_urls.add(url)
            unique_brand_urls.append((brand, url))
        else:
            duplicates.append((brand, url))

    #all_brands_df = pd.DataFrame(brand_urls, columns=['Brand', 'URL'])
    #duplicates_df = pd.DataFrame(duplicates, columns=['Brand', 'URL'])
    #all_brands_without_duplicates_df = pd.DataFrame(unique_brand_urls, columns=['Brand', 'URL'])

    print(f"Total number of unique brands: {len(unique_brand_urls)}")

    scraped_brands = 0
    scraped_brands_list = []
    missed_brands_list = []
    missed_url_list = []
    all_data = []

    async with aiohttp.ClientSession() as session:
        for brand, url in unique_brand_urls[0:10]:  # Limiting to first 10 for testing
            try:
                response = await aux_functions.fetch(session, url)
                soup = BeautifulSoup(response, 'html.parser')

                fragrance_data = scrape_fragrances(soup, base_url, brand)
                if not fragrance_data.empty:
                    print(f"Scraped data for {brand}:")
                    all_data.append(fragrance_data)
                    scraped_brands += 1
                    scraped_brands_list.append(brand)
                else:
                    missed_brands_list.append(brand)
                    missed_url_list.append(url)
                    print(f"No data found for {brand}")
            except Exception as e:
                print(f"Failed to scrape brand {brand}: {e}")

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df['Quantity (ml)'] = pd.to_numeric(full_df['Quantity (ml)'], downcast='integer', errors='coerce')
        full_df['Quantity (ml)'] = full_df['Quantity (ml)'].replace('set', 0)
        full_df['Quantity (ml)'] = full_df['Quantity (ml)'].fillna(0).astype(int)  # Replace NaN with 0 and convert to int
        aux_functions.scrape_to_db(full_df, 'test_PT_fragrances', 'Perfumes24h')
        #aux_functions.scrape_to_excel(full_df, data_dir, 'Perfumes24h Test ')
        if missed_brands_list:
            print(f"Missed brands: {missed_brands_list}")
        if missed_url_list:
            print(f"Missed URLs: {missed_url_list}")

if __name__ == '__main__':
    asyncio.run(main())
