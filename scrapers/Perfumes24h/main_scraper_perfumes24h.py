import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import nest_asyncio
from datetime import datetime
import db_utils  # Ensure this module is correctly implemented

nest_asyncio.apply()


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()


def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return ascii_text


def construct_brand_url(brand_name):
    # Normalize the brand name to remove accents
    brand_name = normalize_text(brand_name)
    # Replace '&' with '-' and remove special characters
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

            # Brand
            brand_name = brand

            # Fragrance Name
            aux_name = product.find('div', class_='tipo_producto').text.strip()
            if aux_name != "":
                fragrance_name = product.find('div', class_='nombre_grupo').text.strip() + " " + aux_name
            else:
                fragrance_name = product.find('div', class_='nombre_grupo').text.strip()

            # Replace fragrance types with abbreviations
            fragrance_name = replace_fragrance_type(fragrance_name)

            # Link
            link_tags = product.find_all('a', href=True)
            if len(link_tags) > 1:
                link = link_tags[1]['href']
            if not link.startswith('http'):
                link = base_url + link

            # Quantity and Price
            variants = product.find_all('div', class_='item_tamanyo')
            for variant in variants:
                quantity_text = variant.text.strip()

                if quantity_text.lower() == 'set':
                    quantity = 'set'
                else:
                    quantity_match = re.search(r'(\d+)\s*ml', quantity_text, re.IGNORECASE)
                    if quantity_match:
                        quantity = float(quantity_match.group(1))
                    else:
                        quantity = 0.0  # Default value if no quantity is found

                price_text = variant.get('data-pp', '0').replace(',', '.')
                price = float(price_text)

                if fragrance_name and price and link:
                    fragrances.append({
                        'Brand': brand_name,
                        'Fragrance Name': fragrance_name,
                        'Quantity': quantity,  # Changed column name to 'Quantity'
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
        response = await fetch(session, url)
        soup = BeautifulSoup(response, 'html.parser')
        brands = []
        brand_divs = soup.find_all('div', id=re.compile('^letra_'))
        for brand_div in brand_divs:
            brand_name = brand_div['data-nombre_marca']
            brands.append(brand_name)
    return brands

def scraped_to_db(fragrances):
    db_name = 'PT_fragrances'
    table_name = 'Perfumes24h'
    db_utils.create_table(db_name, table_name)
    fragrances_tuples = [tuple(row) for row in fragrances[['Brand', 'Fragrance Name', 'Quantity', 'Price (€)', 'Link', 'Website']].to_records(index=False)]
    db_utils.insert_multiple_fragrances(db_name, table_name, fragrances_tuples)
    print("Data has been inserted into the database")

def scrape_to_excel(fragrances):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f'24h_fragrances_PT_{timestamp}.xlsx'
    fragrances.to_excel(filename, index=False)
    path = r"D:\Drive Folder\FragrancesV2\fragrancePT_Cleaner\fragranceDB\scrapers\Perfumes24h"
    print(filename + " has been saved in " + path)

async def main():
    base_url = "https://perfumes24h.com/"
    brands_url = "https://perfumes24h.com/perfumes/"

    # Dictionary to map special cases of brand names to URLs
    special_urls = {
        'Aguilera': 'https://perfumes24h.com/perfumes/christina-aguilera/',
        'Annayake': 'https://perfumes24h.com/perfumes-11/',
        'Arden': 'https://perfumes24h.com/perfumes/elizabeth-arden/',
        'Banani': 'https://perfumes24h.com/perfumes/bruno-banani/',
        'Basi': 'https://perfumes24h.com/perfumes/armand-basi/',
        'Biagiotti': 'https://perfumes24h.com/perfumes/laura-biagiotti/',
        'Boss': 'https://perfumes24h.com/perfumes/hugo-boss/',
        'Cavalli': 'https://perfumes24h.com/perfumes/roberto-cavalli/',
        'Christian dior': 'https://perfumes24h.com/perfumes/christian-dior/',
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
        'Herrera': 'https://perfumes24h.com/perfumes/herrera/',
        'Hilfiger': 'https://perfumes24h.com/perfumes/hilfiger/',
        'Hilton': 'https://perfumes24h.com/perfumes/hilton/',
        'Jeanne arthes': 'https://perfumes24h.com/perfumes/jeanne-arthes/',
        'Jessica parker': 'https://perfumes24h.com/perfumes/sarah-jessica-parker/',
        'Jesús del pozo': 'https://perfumes24h.com/perfumes/halloween/',
        'Kardashian': 'https://perfumes24h.com/perfumes/kim-kardashian',
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

    # Get all brands
    brands = await get_all_brands(brands_url)
    # Replace brands with their special URLs if they exist in the dictionary
    brand_urls = [(brand, special_urls.get(brand, construct_brand_url(brand))) for brand in brands]

    print(f"Total number of brands: {len(brands)}")
    scraped_brands = 0
    scraped_brands_list = []
    missed_brands_list = []
    missed_url_list = []
    all_data = []

    async with aiohttp.ClientSession() as session:
        for brand, url in brand_urls:  # Limiting to first 10 for testing
            #print(url)
            try:
                response = await fetch(session, url)
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
        scraped_to_db(full_df)  # Insert into DB
        #scrape_to_excel(full_df)
        #with pd.option_context('display.max_rows', None, 'display.max_columns',
                               #None):  # more options can be specified also
            #print(full_df)
        print(missed_brands_list)
        print(missed_url_list)
        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #print(full_df)
        # full_df.to_csv("scraped_fragrances.csv", index=False)
        # print("All data scraped and saved to scraped_fragrances.csv")


if __name__ == '__main__':
    asyncio.run(main())
